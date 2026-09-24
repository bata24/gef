#define _GNU_SOURCE

#include <errno.h>
#include <linux/io_uring.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>

#ifndef __NR_io_uring_setup
#define __NR_io_uring_setup 425
#define __NR_io_uring_enter 426
#define __NR_io_uring_register 427
#endif

/* Newer UAPI values are defined here so that old headers still build this file. */
#define TEST_SETUP_NO_MMAP (1U << 14)
#define TEST_SETUP_SQE128 (1U << 10)
#define TEST_SETUP_CQE32 (1U << 11)
#define TEST_FEAT_SINGLE_MMAP (1U << 0)
#define TEST_OFF_PBUF_RING 0x80000000ULL
#define TEST_REGISTER_PBUF_RING 22
#define TEST_PBUF_RING_MMAP 1

struct test_buf_reg {
    uint64_t ring_addr;
    uint32_t ring_entries;
    uint16_t bgid;
    uint16_t flags;
    uint64_t resv[3];
};

struct ring {
    int fd;
    struct io_uring_params p;
    void *sq;
    void *cq;
    void *sqes;
    size_t sqe_size;
    size_t sq_size;
    size_t cq_size;
};

void *no_mmap_rings;
void *no_mmap_sqes;

static int setup(unsigned entries, struct io_uring_params *p)
{
    return syscall(__NR_io_uring_setup, entries, p);
}

static int enter(int fd, unsigned to_submit, unsigned min_complete)
{
    return syscall(__NR_io_uring_enter, fd, to_submit, min_complete, IORING_ENTER_GETEVENTS, NULL, 0);
}

static void *map(int fd, size_t size, uint64_t offset)
{
    void *p = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_POPULATE, fd, offset);
    if (p == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
    return p;
}

/* Map like liburing; split forces separate SQ/CQ mappings even with IORING_FEAT_SINGLE_MMAP. */
static void open_ring(struct ring *r, unsigned entries, int split)
{
    memset(r, 0, sizeof(*r));
    r->fd = setup(entries, &r->p);
    if (r->fd < 0) {
        perror("io_uring_setup");
        exit(1);
    }
    r->sq_size = r->p.sq_off.array + r->p.sq_entries * sizeof(uint32_t);
    r->cq_size = r->p.cq_off.cqes + r->p.cq_entries * sizeof(struct io_uring_cqe);
    int single = (r->p.features & TEST_FEAT_SINGLE_MMAP) && !split;
    if (single) {
        if (r->cq_size > r->sq_size)
            r->sq_size = r->cq_size;
        r->cq_size = r->sq_size;
    }
    r->sq = map(r->fd, r->sq_size, IORING_OFF_SQ_RING);
    r->cq = single ? r->sq : map(r->fd, r->cq_size, IORING_OFF_CQ_RING);
    r->sqes = map(r->fd, r->p.sq_entries * sizeof(struct io_uring_sqe), IORING_OFF_SQES);
    r->sqe_size = sizeof(struct io_uring_sqe);
}

static void submit_nops(struct ring *r, unsigned n)
{
    uint32_t *tail = (uint32_t *)((char *)r->sq + r->p.sq_off.tail);
    uint32_t mask = *(uint32_t *)((char *)r->sq + r->p.sq_off.ring_mask);
    uint32_t *array = (uint32_t *)((char *)r->sq + r->p.sq_off.array);
    for (unsigned i = 0; i < n; i++) {
        unsigned index = (*tail + i) & mask;
        struct io_uring_sqe *sqe = (struct io_uring_sqe *)((char *)r->sqes + index * r->sqe_size);
        memset(sqe, 0, r->sqe_size);
        sqe->opcode = IORING_OP_NOP;
        sqe->user_data = 0x4745460000000000ULL + i;
        array[index] = index;
    }
    __atomic_store_n(tail, *tail + n, __ATOMIC_RELEASE);
    if (enter(r->fd, n, n) != (int)n) {
        perror("io_uring_enter");
        exit(1);
    }
}

static void print_ring(const char *name, struct ring *r)
{
    printf("%s fd=%d features=%#x sq_entries=%u cq_entries=%u sq=%p cq=%p sqes=%p sq_size=%#zx cq_size=%#zx\n",
           name, r->fd, r->p.features, r->p.sq_entries, r->p.cq_entries, r->sq, r->cq, r->sqes,
           r->sq_size, r->cq_size);
}

int main(void)
{
    struct ring a, b, e;
    long page = sysconf(_SC_PAGESIZE);

    /* A: an ordinary ring with completed requests. */
    open_ring(&a, 4, 0);
    submit_nops(&a, 3);
    print_ring("A", &a);

    /* B: an unreadable ring (LOG-002). */
    open_ring(&b, 4, 1);
    submit_nops(&b, 1);
    print_ring("B", &b);
    if (mprotect(b.sq, b.sq_size, PROT_NONE) || mprotect(b.cq, b.cq_size, PROT_NONE) ||
        mprotect(b.sqes, b.p.sq_entries * sizeof(struct io_uring_sqe), PROT_NONE)) {
        perror("mprotect");
        return 1;
    }

    /* E: a larger ring whose SQ mapping is split in two VMAs. */
    open_ring(&e, 256, 1);
    submit_nops(&e, 5);
    print_ring("E", &e);
    if (e.sq_size > (size_t)page && mprotect((char *)e.sq + page, page, PROT_READ)) {
        perror("mprotect");
        return 1;
    }

    /* C: IORING_SETUP_NO_MMAP (Linux v6.5-) with user memory. */
    size_t no_mmap_size = 16 * page;
    char *mem = mmap(NULL, no_mmap_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_POPULATE, -1, 0);
    if (mem == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    struct ring c;
    memset(&c, 0, sizeof(c));
    c.p.flags = TEST_SETUP_NO_MMAP;
    /* user_addr of both offsets is at +32; old headers named it resv. */
    *(uint64_t *)((char *)&c.p.sq_off + 32) = (uintptr_t)mem;
    *(uint64_t *)((char *)&c.p.cq_off + 32) = (uintptr_t)(mem + 4 * page);
    c.fd = setup(8, &c.p);
    if (c.fd >= 0) {
        c.sqes = mem;
        c.sqe_size = sizeof(struct io_uring_sqe);
        c.sq = c.cq = mem + 4 * page;
        no_mmap_rings = c.sq;
        no_mmap_sqes = c.sqes;
        submit_nops(&c, 2);
        print_ring("C", &c);
    } else {
        printf("C unsupported errno=%d\n", errno);
    }

    /* F: IORING_SETUP_NO_MMAP laid out like liburing, with 128-byte SQEs and 32-byte CQEs. */
    char *fmem = mmap(NULL, 8 * page, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_POPULATE, -1, 0);
    if (fmem == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    struct ring f;
    memset(&f, 0, sizeof(f));
    size_t f_sqes_size = (64 * 128 + page - 1) & ~(page - 1);
    f.p.flags = TEST_SETUP_NO_MMAP | TEST_SETUP_SQE128 | TEST_SETUP_CQE32;
    *(uint64_t *)((char *)&f.p.sq_off + 32) = (uintptr_t)fmem;
    *(uint64_t *)((char *)&f.p.cq_off + 32) = (uintptr_t)(fmem + f_sqes_size);
    f.fd = setup(64, &f.p);
    if (f.fd >= 0) {
        f.sqes = fmem;
        f.sqe_size = 128;
        f.sq = f.cq = fmem + f_sqes_size;
        /* liburing fills sq_array with 0, 1, 2, ... */
        uint32_t *f_array = (uint32_t *)((char *)f.sq + f.p.sq_off.array);
        for (unsigned i = 0; i < f.p.sq_entries; i++)
            f_array[i] = i;
        submit_nops(&f, 3);
        print_ring("F", &f);
        printf("F sq_array=+%#x\n", f.p.sq_off.array);
    } else {
        printf("F unsupported errno=%d\n", errno);
    }

    /* D: a provided buffer ring mapped by IORING_OFF_PBUF_RING (Linux v6.4-). */
    struct test_buf_reg reg;
    memset(&reg, 0, sizeof(reg));
    reg.ring_entries = 8;
    reg.bgid = 3;
    reg.flags = TEST_PBUF_RING_MMAP;
    if (syscall(__NR_io_uring_register, a.fd, TEST_REGISTER_PBUF_RING, &reg, 1) == 0) {
        void *pbuf = map(a.fd, 8 * 16, TEST_OFF_PBUF_RING | (3ULL << 16));
        printf("D pbuf=%p bgid=3\n", pbuf);
    } else {
        printf("D unsupported errno=%d\n", errno);
    }

    fflush(stdout);
    kill(getpid(), SIGTRAP);

    /* The inferior must be intact after the dump. */
    uint32_t *a_cq_tail = (uint32_t *)((char *)a.cq + a.p.cq_off.tail);
    printf("after: A cq tail=%u\n", *a_cq_tail);
    puts(*a_cq_tail == 3 ? "TEST-OK" : "TEST-NG");
    return 0;
}
