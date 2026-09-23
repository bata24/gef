#define _GNU_SOURCE
#include <setjmp.h>
#include <signal.h>
#include <stdio.h>

jmp_buf g_env;          // [1] setjmp: mask not saved
sigjmp_buf g_sigenv;    // [2] sigsetjmp(.., 1): mask saved
sigjmp_buf g_regenv;    // [3] pattern values in callee-saved registers
jmp_buf g_zero;         // [5] never initialized (all zero)

volatile long seed[12];

// Called through a pointer so that it is not treated as returns_twice and live values stay in registers
int (*volatile sj)(struct __jmp_buf_tag *, int) = __sigsetjmp;

static void on_trap(int sig)
{
    (void)sig;
}

// Stop with int3 after printing the label; buf is in $rdi ($edi on i386)
__attribute__((noinline)) void stop_here(void *buf, const char *label)
{
    printf("[stop] %-28s buf=%p\n", label, buf);
    fflush(stdout);
#if defined(__x86_64__) || defined(__i386__)
    __asm__ volatile("int3" :: "D"(buf) : "memory");
#else
    raise(SIGTRAP);
#endif
}

// [4] longjmp from two frames deeper to a jmp_buf on the stack
__attribute__((noinline)) static void deep2(jmp_buf env)
{
    stop_here(env, "4: before longjmp (stack)");
    longjmp(env, 42);
}

__attribute__((noinline)) static void deep1(jmp_buf env)
{
    deep2(env);
    puts("unreachable");
}

static void test_stack(void)
{
    jmp_buf local;
    volatile int r = setjmp(local);
    if (r == 0) {
        stop_here(local, "4: stack jmp_buf");
        deep1(local);
    }
    printf("[4] returned by longjmp: %d\n", r);
}

int main(void)
{
    signal(SIGTRAP, on_trap);
    printf("g_env=%p g_sigenv=%p g_regenv=%p g_zero=%p\n",
           (void *)g_env, (void *)g_sigenv, (void *)g_regenv, (void *)g_zero);

    // [1] setjmp: __mask_was_saved = 0
    if (setjmp(g_env) == 0)
        stop_here(g_env, "1: setjmp (no mask)");

    // [2] block SIGUSR1/SIGTERM, then sigsetjmp(.., 1)
    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, SIGUSR1);
    sigaddset(&set, SIGTERM);
    sigprocmask(SIG_BLOCK, &set, NULL);
    volatile int back = sigsetjmp(g_sigenv, 1);
    if (back) {
        // back from [6]: SIGUSR1/SIGTERM should be blocked again
        sigset_t cur;
        sigprocmask(SIG_BLOCK, NULL, &cur);
        printf("[6] back from siglongjmp: SIGUSR1 %s\n", sigismember(&cur, SIGUSR1) ? "blocked" : "unblocked");
        return 0;
    }
    stop_here(g_sigenv, "2: sigsetjmp (mask saved)");

    // [3] save while callee-saved registers hold 0x10203040 + 0x01010101 * i
    for (int i = 0; i < 12; i++)
        seed[i] = (long)(0x10203040UL + 0x01010101UL * i);
    long a0 = seed[0], a1 = seed[1], a2 = seed[2], a3 = seed[3], a4 = seed[4], a5 = seed[5];
    long a6 = seed[6], a7 = seed[7], a8 = seed[8], a9 = seed[9], a10 = seed[10], a11 = seed[11];
    sj(g_regenv, 1);
    stop_here(g_regenv, "3: callee-saved patterns");
    printf("%lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx %lx\n", a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11);

    // [4] buffer on the stack and a real longjmp
    test_stack();

    // [5] uninitialized buffer: mangled fields should be shown as 0
    stop_here(g_zero, "5: zero buffer");

    // [6] unblock, then siglongjmp back to [2] (the saved mask is restored)
    sigprocmask(SIG_UNBLOCK, &set, NULL);
    stop_here(g_sigenv, "6: before siglongjmp");
    siglongjmp(g_sigenv, 1);
}
