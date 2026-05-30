// gcc -O0 test.c

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/syscall.h>
#include <sys/uio.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <sys/types.h>

#ifndef HAVE_STRUCT_MMSGHDR
struct fallback_mmsghdr {
    struct msghdr msg_hdr;
    unsigned int  msg_len;
};
#endif

#ifndef RWF_HIPRI
#define RWF_HIPRI 0x00000001
#endif

#if defined(__i386__) || (defined(__arm__) && !defined(__aarch64__)) || \
    (defined(__riscv) && __riscv_xlen == 32) || defined(__powerpc__) && !defined(__powerpc64__)
#  define SYS_RW_32BIT_OFF 1
#else
#  define SYS_RW_32BIT_OFF 0
#endif

#if SYS_RW_32BIT_OFF
#  define POFF_LO(off) ((unsigned long)((unsigned long long)(off) & 0xffffffffUL))
#  define POFF_HI(off) ((unsigned long)((unsigned long long)(off) >> 32))
#  define SYS_PWRITE64(fd, buf, cnt, off) \
       syscall(SYS_pwrite64, (fd), (buf), (cnt), POFF_LO(off), POFF_HI(off))
#  define SYS_PREAD64(fd, buf, cnt, off) \
       syscall(SYS_pread64, (fd), (buf), (cnt), POFF_LO(off), POFF_HI(off))
#else
#  define SYS_PWRITE64(fd, buf, cnt, off) \
       syscall(SYS_pwrite64, (fd), (buf), (cnt), (off))
#  define SYS_PREAD64(fd, buf, cnt, off) \
       syscall(SYS_pread64, (fd), (buf), (cnt), (off))
#endif

static const char *TMP_TEMPLATE = "/tmp/xtap_test_XXXXXX";

static void banner(const char *tag, int fd) {
    char buf[128];
    int n = snprintf(buf, sizeof(buf), "\n=== %s (fd=%d) ===\n", tag, fd);
    if (n > 0)
        syscall(SYS_write, 1, buf, (size_t)n);
}

static void die(const char *what) {
    perror(what);
    exit(1);
}

static void soft_fail(const char *what) {
    perror(what);
}

static void test_write_read(void) {
    char path[64];
    strcpy(path, TMP_TEMPLATE);
    int fd = mkstemp(path);
    if (fd < 0)
        die("mkstemp");
    unlink(path); /* keep it anonymous on disk; fd stays valid */

    const char *msg = "hello-write-read";
    banner("write", fd);
    if (syscall(SYS_write, fd, msg, strlen(msg)) < 0)
        soft_fail("SYS_write");

    /* rewind and read it back */
    lseek(fd, 0, SEEK_SET);

    char rbuf[64] = {0};
    banner("read", fd);
    if (syscall(SYS_read, fd, rbuf, sizeof(rbuf)) < 0)
        soft_fail("SYS_read");

    close(fd);
}

static void test_pwrite_pread(void) {
    char path[64];
    strcpy(path, TMP_TEMPLATE);
    int fd = mkstemp(path);
    if (fd < 0)
        die("mkstemp");
    unlink(path);

    const char *msg = "hello-pwrite-pread";
    off_t off = 16; /* write at a non-zero offset, no lseek */

    banner("pwrite64", fd);
    if (SYS_PWRITE64(fd, msg, strlen(msg), off) < 0)
        soft_fail("SYS_pwrite64");

    char rbuf[64] = {0};
    banner("pread64", fd);
    if (SYS_PREAD64(fd, rbuf, sizeof(rbuf), off) < 0)
        soft_fail("SYS_pread64");

    close(fd);
}

static void test_writev_readv(void) {
    char path[64];
    strcpy(path, TMP_TEMPLATE);
    int fd = mkstemp(path);
    if (fd < 0)
        die("mkstemp");
    unlink(path);

    struct iovec wiov[2];
    wiov[0].iov_base = (void *)"writev-part1:";
    wiov[0].iov_len = strlen("writev-part1:");
    wiov[1].iov_base = (void *)"writev-part2";
    wiov[1].iov_len = strlen("writev-part2");

    banner("writev", fd);
    if (syscall(SYS_writev, fd, wiov, 2) < 0)
        soft_fail("SYS_writev");

    lseek(fd, 0, SEEK_SET);

    char b0[16] = {0};
    char b1[16] = {0};
    struct iovec riov[2];
    riov[0].iov_base = b0;
    riov[0].iov_len = sizeof(b0);
    riov[1].iov_base = b1;
    riov[1].iov_len = sizeof(b1);

    banner("readv", fd);
    if (syscall(SYS_readv, fd, riov, 2) < 0)
        soft_fail("SYS_readv");

    close(fd);
}

static void test_pwritev_preadv(void) {
    char path[64];
    strcpy(path, TMP_TEMPLATE);
    int fd = mkstemp(path);
    if (fd < 0)
        die("mkstemp");
    unlink(path);

    off_t off = 32;

    struct iovec wiov[2];
    wiov[0].iov_base = (void *)"pwritev-a:";
    wiov[0].iov_len = strlen("pwritev-a:");
    wiov[1].iov_base = (void *)"pwritev-b";
    wiov[1].iov_len = strlen("pwritev-b");

    /*
     * preadv/pwritev split the 64-bit offset into pos_l/pos_h on some ABIs.
     * On x86-64 the offset is passed as two args (low, high); glibc's syscall()
     * forwards args verbatim, so pass low then high explicitly.
     */
    unsigned long pos_l = (unsigned long)(off & 0xffffffff);
    unsigned long pos_h = (unsigned long)((unsigned long long)off >> 32);

    banner("pwritev", fd);
    if (syscall(SYS_pwritev, fd, wiov, 2, pos_l, pos_h) < 0)
        soft_fail("SYS_pwritev");

    char b0[16] = {0};
    char b1[16] = {0};
    struct iovec riov[2];
    riov[0].iov_base = b0;
    riov[0].iov_len = sizeof(b0);
    riov[1].iov_base = b1;
    riov[1].iov_len = sizeof(b1);

    banner("preadv", fd);
    if (syscall(SYS_preadv, fd, riov, 2, pos_l, pos_h) < 0)
        soft_fail("SYS_preadv");

    close(fd);
}

static void test_pwritev2_preadv2(void) {
    char path[64];
    strcpy(path, TMP_TEMPLATE);
    int fd = mkstemp(path);
    if (fd < 0)
        die("mkstemp");
    unlink(path);

    off_t off = 48;

    struct iovec wiov[2];
    wiov[0].iov_base = (void *)"pwritev2-x:";
    wiov[0].iov_len = strlen("pwritev2-x:");
    wiov[1].iov_base = (void *)"pwritev2-y";
    wiov[1].iov_len = strlen("pwritev2-y");

    unsigned long pos_l = (unsigned long)(off & 0xffffffff);
    unsigned long pos_h = (unsigned long)((unsigned long long)off >> 32);
    int flags = 0; /* RWF_* flags; 0 = same semantics as pwritev */

    banner("pwritev2", fd);
    if (syscall(SYS_pwritev2, fd, wiov, 2, pos_l, pos_h, flags) < 0)
        soft_fail("SYS_pwritev2");

    char b0[16] = {0};
    char b1[16] = {0};
    struct iovec riov[2];
    riov[0].iov_base = b0;
    riov[0].iov_len = sizeof(b0);
    riov[1].iov_base = b1;
    riov[1].iov_len = sizeof(b1);

    banner("preadv2", fd);
    if (syscall(SYS_preadv2, fd, riov, 2, pos_l, pos_h, flags) < 0)
        soft_fail("SYS_preadv2");

    close(fd);
}

static void run_file_tests(void) {
    test_write_read();
    test_pwrite_pread();
    test_writev_readv();
    test_pwritev_preadv();
    test_pwritev2_preadv2();
}

static void client_send(int fd) {
    /* sendto: datagram with explicit (NULL) destination on a connected pair */
    const char *m1 = "sendto-datagram";
    banner("sendto", fd);
    if (syscall(SYS_sendto, fd, m1, strlen(m1), 0, NULL, 0) < 0)
        soft_fail("SYS_sendto");

    /* sendmsg: single iovec inside a msghdr */
    const char *m2 = "sendmsg-datagram";
    struct iovec iov;
    iov.iov_base = (void *)m2;
    iov.iov_len = strlen(m2);
    struct msghdr mh;
    memset(&mh, 0, sizeof(mh));
    mh.msg_iov = &iov;
    mh.msg_iovlen = 1;
    banner("sendmsg", fd);
    if (syscall(SYS_sendmsg, fd, &mh, 0) < 0)
        soft_fail("SYS_sendmsg");

    /* sendmmsg: two datagrams in one call */
    const char *a = "sendmmsg-#1:";
    const char *b = "sendmmsg-#2";
    struct iovec iov1, iov2;
    iov1.iov_base = (void *)a;
    iov1.iov_len = strlen(a);
    iov2.iov_base = (void *)b;
    iov2.iov_len = strlen(b);

    struct mmsghdr mm[2];
    memset(mm, 0, sizeof(mm));
    mm[0].msg_hdr.msg_iov = &iov1;
    mm[0].msg_hdr.msg_iovlen = 1;
    mm[1].msg_hdr.msg_iov = &iov2;
    mm[1].msg_hdr.msg_iovlen = 1;

    banner("sendmmsg", fd);
    if (syscall(SYS_sendmmsg, fd, mm, 2, 0) < 0)
        soft_fail("SYS_sendmmsg");
}

static void server_recv(int fd) {
    char buf[64];

    /* recvfrom: matches the sendto datagram */
    memset(buf, 0, sizeof(buf));
    banner("recvfrom", fd);
    if (syscall(SYS_recvfrom, fd, buf, sizeof(buf), 0, NULL, NULL) < 0)
        soft_fail("SYS_recvfrom");

    /* recvmsg: matches the sendmsg datagram */
    struct iovec iov;
    memset(buf, 0, sizeof(buf));
    iov.iov_base = buf;
    iov.iov_len = sizeof(buf);
    struct msghdr mh;
    memset(&mh, 0, sizeof(mh));
    mh.msg_iov = &iov;
    mh.msg_iovlen = 1;
    banner("recvmsg", fd);
    if (syscall(SYS_recvmsg, fd, &mh, 0) < 0)
        soft_fail("SYS_recvmsg");

    /* recvmmsg: matches the two sendmmsg datagrams */
    char b0[64], b1[64];
    memset(b0, 0, sizeof(b0));
    memset(b1, 0, sizeof(b1));
    struct iovec iov0, iov1;
    iov0.iov_base = b0;
    iov0.iov_len = sizeof(b0);
    iov1.iov_base = b1;
    iov1.iov_len = sizeof(b1);

    struct mmsghdr mm[2];
    memset(mm, 0, sizeof(mm));
    mm[0].msg_hdr.msg_iov = &iov0;
    mm[0].msg_hdr.msg_iovlen = 1;
    mm[1].msg_hdr.msg_iov = &iov1;
    mm[1].msg_hdr.msg_iovlen = 1;

    /* timeout NULL = block until at least one datagram; we expect two. */
    banner("recvmmsg", fd);
    if (syscall(SYS_recvmmsg, fd, mm, 2, 0, NULL) < 0)
        soft_fail("SYS_recvmmsg");
}

static void run_socket_tests(void) {
    int sv[2];
    if (socketpair(AF_UNIX, SOCK_DGRAM, 0, sv) < 0)
        die("socketpair");

    pid_t pid = fork();
    if (pid < 0)
        die("fork");

    if (pid == 0) {
        /* child = client/sender */
        close(sv[0]);
        client_send(sv[1]);
        close(sv[1]);
        _exit(0);
    }

    /* parent = server/receiver */
    close(sv[1]);
    server_recv(sv[0]);
    close(sv[0]);

    int status;
    waitpid(pid, &status, 0);
}

int main(int argc, char **argv) {
    const char *mode = (argc > 1) ? argv[1] : "all";

    if (strcmp(mode, "file") == 0) {
        run_file_tests();
    } else if (strcmp(mode, "socket") == 0) {
        run_socket_tests();
    } else if (strcmp(mode, "all") == 0) {
        run_file_tests();
        run_socket_tests();
    } else {
        fprintf(stderr, "usage: %s [all|file|socket]\n", argv[0]);
        return 2;
    }

    syscall(SYS_write, 1, "\n=== done ===\n", 14);
    return 0;
}
