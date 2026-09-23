// gcc -O0 -g test.c
#define _GNU_SOURCE
#include <ucontext.h>
#include <stdio.h>
#include <unistd.h>

static ucontext_t ctx_main, ctx_a, ctx_b;
static char stack_a[64 * 1024];
static char stack_b[64 * 1024];

static void func_a(void)
{
    unsigned long i = 0;
    while (1) {
        printf("[A] tick %lu\n", i++);
        fflush(stdout);
        sleep(1);
        swapcontext(&ctx_a, &ctx_b); /* save A into ctx_a, resume B */
    }
}

static void func_b(void)
{
    unsigned long i = 0;
    while (1) {
        printf("[B] tick %lu\n", i++);
        fflush(stdout);
        sleep(1);
        swapcontext(&ctx_b, &ctx_a); /* save B into ctx_b, resume A */
    }
}

int main(void)
{
    printf("pid          = %d\n", getpid());
    printf("ctx_main     = %p\n", (void *)&ctx_main);
    printf("ctx_a        = %p  (stack %p)\n", (void *)&ctx_a, (void *)stack_a);
    printf("ctx_b        = %p  (stack %p)\n", (void *)&ctx_b, (void *)stack_b);
    printf("attach with gdb, then e.g.: ucontext %p\n", (void *)&ctx_a);
    fflush(stdout);

    getcontext(&ctx_a);
    ctx_a.uc_stack.ss_sp = stack_a;
    ctx_a.uc_stack.ss_size = sizeof(stack_a);
    ctx_a.uc_link = &ctx_main;
    makecontext(&ctx_a, func_a, 0);

    getcontext(&ctx_b);
    ctx_b.uc_stack.ss_sp = stack_b;
    ctx_b.uc_stack.ss_size = sizeof(stack_b);
    ctx_b.uc_link = &ctx_main;
    makecontext(&ctx_b, func_b, 0);

    swapcontext(&ctx_main, &ctx_a); /* never returns (funcs loop forever) */
    return 0;
}
