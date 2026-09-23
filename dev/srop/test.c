// gcc -O0 -g -no-pie -fno-stack-protector test.c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/syscall.h>

/* kernel struct sigcontext_64 */
struct sigctx {
    uint64_t r8, r9, r10, r11, r12, r13, r14, r15;
    uint64_t rdi, rsi, rbp, rbx, rdx, rax, rcx, rsp, rip, eflags;
    uint16_t cs, gs, fs, ss;
    uint64_t err, trapno, oldmask, cr2;
    uint64_t fpstate;
    uint64_t reserved[8];
};

/* kernel struct rt_sigframe (enough of it for rt_sigreturn) */
struct rt_sigframe {
    uint64_t pretcode;
    uint64_t uc_flags;
    uint64_t uc_link;
    struct { void *ss_sp; int ss_flags; uint64_t ss_size; } uc_stack;
    struct sigctx uc_mcontext;
    uint64_t uc_sigmask;
    uint64_t info[16];
};

static char newstack[16 * 1024];

static void restored(void)
{
    printf("[+] rt_sigreturn landed in restored(); registers were restored from the frame\n");
    _exit(0);
}

int main(void)
{
    static struct rt_sigframe f;
    uint16_t cs, ss;

    memset(&f, 0, sizeof(f));
    __asm__ volatile("mov %%cs, %0; mov %%ss, %1" : "=r"(cs), "=r"(ss));

    f.pretcode = 0xdeadc0dedeadc0de;       /* return-address slot, ignored by rt_sigreturn */
    f.uc_flags = 0;
    f.uc_stack.ss_flags = 2;               /* SS_DISABLE, just to show something non-zero */
    f.uc_mcontext.rdi = 0x1111111111111111;
    f.uc_mcontext.rsi = 0x2222222222222222;
    f.uc_mcontext.rdx = 0x3333333333333333;
    f.uc_mcontext.rcx = 0x4444444444444444;
    f.uc_mcontext.r8  = 0x0808080808080808;
    f.uc_mcontext.r15 = 0x1515151515151515;
    f.uc_mcontext.rip = (uint64_t)&restored;
    f.uc_mcontext.rsp = (uint64_t)(newstack + sizeof(newstack));
    f.uc_mcontext.eflags = 0x202;
    f.uc_mcontext.cs = cs;
    f.uc_mcontext.ss = ss;
    f.uc_mcontext.fpstate = 0;             /* NULL: no FP/xmm restore */
    f.uc_sigmask = 0;

    printf("pid           = %d\n", getpid());
    printf("rt_sigframe   = %p   <- gef> sigreturn %p\n", (void *)&f, (void *)&f);
    printf("  &uc         = %p   (rsp at the syscall; sigreturn $rsp-8)\n", (void *)&f.uc_flags);
    printf("  &uc_mcontext= %p   <- gef> ucontext -m %p\n", (void *)&f.uc_mcontext, (void *)&f.uc_mcontext);
    printf("  restored()  = %p\n", (void *)&restored);
    fflush(stdout);

    /* rax = rt_sigreturn, rsp = &uc, trap, then the syscall */
    register long rax __asm__("rax") = SYS_rt_sigreturn;
    __asm__ volatile(
        "mov %0, %%rsp\n\t"
        "int3\n\t"
        "syscall\n\t"
        :
        : "r"((uint64_t)&f.uc_flags), "r"(rax)
        : "memory");
    return 0;
}
