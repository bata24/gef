# GEF Commands

## Table of contents

- [01-a. Debugging Support - Context](#01-a-debugging-support---context)
- [01-b. Debugging Support - Breakpoint](#01-b-debugging-support---breakpoint)
- [01-c. Debugging Support - Basic Command Extension](#01-c-debugging-support---basic-command-extension)
- [01-d. Debugging Support - Execution](#01-d-debugging-support---execution)
- [01-e. Debugging Support - Assemble](#01-e-debugging-support---assemble)
- [01-f. Debugging Support - Context Extension](#01-f-debugging-support---context-extension)
- [01-g. Debugging Support - Syscall](#01-g-debugging-support---syscall)
- [01-h. Debugging Support - Emulation](#01-h-debugging-support---emulation)
- [01-i. Debugging Support - Other](#01-i-debugging-support---other)
- [02-a. Process Information - General](#02-a-process-information---general)
- [02-b. Process Information - Base Address](#02-b-process-information---base-address)
- [02-c. Process Information - Memory/Section](#02-c-process-information---memorysection)
- [02-d. Process Information - Trivial Information](#02-d-process-information---trivial-information)
- [02-e. Process Information - Complex Structure Information](#02-e-process-information---complex-structure-information)
- [02-f. Process Information - Security](#02-f-process-information---security)
- [02-g. Process Information - Symbol](#02-g-process-information---symbol)
- [02-h. Process Information - Type](#02-h-process-information---type)
- [03-a. Memory - Search](#03-a-memory---search)
- [03-b. Memory - View](#03-b-memory---view)
- [03-c. Memory - Compare](#03-c-memory---compare)
- [03-d. Memory - Patch](#03-d-memory---patch)
- [03-e. Memory - Calculation](#03-e-memory---calculation)
- [03-f. Memory - Dump/Load](#03-f-memory---dumpload)
- [03-g. Memory - Investigation](#03-g-memory---investigation)
- [04-a. Register - View](#04-a-register---view)
- [04-b. Register - Modify](#04-b-register---modify)
- [05-a. Heap - Glibc](#05-a-heap---glibc)
- [05-b. Heap - Chromium/V8](#05-b-heap---chromiumv8)
- [05-c. Heap - Other](#05-c-heap---other)
- [06-a. Qemu-system/KGDB Cooperation - Memory Map](#06-a-qemu-systemkgdb-cooperation---memory-map)
- [06-b. Qemu-system/KGDB Cooperation - Register](#06-b-qemu-systemkgdb-cooperation---register)
- [06-c. Qemu-system/KGDB Cooperation - Linux Basic](#06-c-qemu-systemkgdb-cooperation---linux-basic)
- [06-d. Qemu-system/KGDB Cooperation - Virt/Phys/Page](#06-d-qemu-systemkgdb-cooperation---virtphyspage)
- [06-e. Qemu-system/KGDB Cooperation - Linux Symbol/Type](#06-e-qemu-systemkgdb-cooperation---linux-symboltype)
- [06-f. Qemu-system/KGDB Cooperation - Linux Task](#06-f-qemu-systemkgdb-cooperation---linux-task)
- [06-g. Qemu-system/KGDB Cooperation - Linux Advanced](#06-g-qemu-systemkgdb-cooperation---linux-advanced)
- [06-h. Qemu-system/KGDB Cooperation - Linux Allocator](#06-h-qemu-systemkgdb-cooperation---linux-allocator)
- [06-i. Qemu-system/KGDB Cooperation - Linux Dynamic Inspection](#06-i-qemu-systemkgdb-cooperation---linux-dynamic-inspection)
- [06-j. Qemu-system/KGDB Cooperation - TrustZone](#06-j-qemu-systemkgdb-cooperation---trustzone)
- [06-k. Qemu-system/KGDB Cooperation - Other](#06-k-qemu-systemkgdb-cooperation---other)
- [07-a. Misc - Conversion](#07-a-misc---conversion)
- [07-b. Misc - Search](#07-b-misc---search)
- [07-c. Misc - Generation](#07-c-misc---generation)
- [07-d. Misc - Show Example](#07-d-misc---show-example)
- [07-e. Misc - Calculation](#07-e-misc---calculation)
- [07-f. Misc - Diff](#07-f-misc---diff)
- [07-g. Misc - Qemu-system](#07-g-misc---qemu-system)
- [99. GEF Maintenance Command](#99-gef-maintenance-command)

# 01-a. Debugging Support - Context
## context

Display various information every time GDB hits a breakpoint.

- Alias: `ctx`

### Syntax

```text
usage: context [-h] [-i] [{legend,regs,stack,code,mem_access,args,source,mem_watch,trace,threads,extra}|{on,off} ...]

positional arguments:
  {legend,regs,stack,code,mem_access,args,source,mem_watch,trace,threads,extra}|{on,off}
                        invoke each pane individually, or temporarily control the output.

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

### Notes

```text
If "on" or "off" is specified, that operation takes precedence.
`context XXX YYY` invokes the `context-XXX` command and then the `context-YYY` command, in that order.
There are various configuration options that modify the behavior of context. You can list them with gef config context.
```

## context-args

Context internal command to display arguments.


### Syntax

```text
usage: context-args [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-code

Context internal command to display code.


### Syntax

```text
usage: context-code [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-extra

Context internal command to display extra information or execute command.


### Syntax

```text
usage: context-extra [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-legend

Context internal command to display the legend.


### Syntax

```text
usage: context-legend [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-mem-access

Context internal command to display accessing memory.

- Alias: `context-mem_access`

### Syntax

```text
usage: context-mem-access [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-mem-watch

Context internal command to display watching memory.

- Alias: `context-mem_watch`

### Syntax

```text
usage: context-mem-watch [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-regs

Context internal command to display registers.


### Syntax

```text
usage: context-regs [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-source

Context internal command to display source.


### Syntax

```text
usage: context-source [-h] [-i] [NB_LINES]

positional arguments:
  NB_LINES              temporarily overrides context_source.nb_lines.

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-stack

Context internal command to display stack.


### Syntax

```text
usage: context-stack [-h] [-i]

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-threads

Context internal command to display threads.


### Syntax

```text
usage: context-threads [-h] [-i] [NB_LINES]

positional arguments:
  NB_LINES              temporarily overrides context_threads.nb_lines.

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## context-trace

Context internal command to display backtrace.


### Syntax

```text
usage: context-trace [-h] [-i] [NB_LINES]

positional arguments:
  NB_LINES              temporarily overrides context_trace.nb_lines.

options:
  -h, --help            show this help message and exit
  -i, --ignore-redirect
                        ignore redirect settings.
```

## dereference

Dereference recursively from an address and display information.

- Alias: `telescope`

### Syntax

```text
usage: dereference [-h] [-a] [-A] [-P PERM] [-z] [-Z] [-m MASK [VALUE ...]] [-M MASK [VALUE ...]] [-t IDX TAG] [-T TAG_OFFSET] [-r] [-f] [-u] [-i INTERVAL] [-d DEPTH] [-D DEPTH_NB_LINES] [-p] [-l] [-s] [-S] [-q] [-Q] [-n] [LOCATION] [NB_LINES]

positional arguments:
  LOCATION              the memory address to dump. (default: current_arch.sp)
  NB_LINES              the count of lines.

options:
  -h, --help            show this help message and exit
  -a, --is-addr         display only valid addresses.
  -A, --is-not-addr     display only invalid addresses.
  -P, --perm PERM       display only specified permission.
  -z, --is-zero         display only zero values.
  -Z, --is-not-zero     display only non-zero values.
  -m, --mask-hits MASK [VALUE ...]
                        display only mask hits.
  -M, --no-mask-hits MASK [VALUE ...]
                        display only mask non-hits.
  -t, --tag IDX TAG     display with tags.
  -T, --tag-offset TAG_OFFSET
                        the slide offset of all tag positions.
  -r, --reverse         display in reverse order line by line.
  -f, --frame-split     display with frame split lines (heuristics).
  -u, --uniq            display with uniq.
  -i, --interval INTERVAL
                        the line number of the interval for showing.
  -d, --depth DEPTH     depth of recursive. (default: 1)
  -D, --depth-nb-lines DEPTH_NB_LINES
                        NB_LINES when recursive. (default: 4)
  -p, --phys            treat LOCATION as a physical address. (qemu-system only)
  -l, --list-head       display if LIST_HEAD or not.
  -s, --slab-contains   display slab_cache name if available.
  -S, --slab-contains-unaligned
                        display slab_cache name (allow unaligned) if available.
  -q, --quiet           do not display other than addresses and values.
  -Q, --quiet-offset    do not display offset and index values.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
dereference                         # dereference $sp 64
dereference $sp 20                  # specify location and number of elements to display
dereference $sp -20                 # display memory backwards
dereference --reverse $sp 20        # display reverse order
dereference --depth 2 $sp 20        # display recursively if valid aligned address
dereference --is-addr $sp 20        # display elements which is valid address
dereference --slab-contains $sp 20  # with slab-contains result (available under qemu-system)
dereference --tag 0 next $sp 20     # with tags
```

### Notes

```text
Use blacklist feature if reading the address causes process crash.
e.g., `gef config dereference.blacklist "[ [0xffffffffc9000000, 0xffffffffc9001000], ]"
then `gef save`.
```

## registers

Display many or all register values from current architecture.

- Alias: `regs`

### Syntax

```text
usage: registers [-h] [-s] [REGISTERS ...]

positional arguments:
  REGISTERS     An array of registers. (default: current_arch.all_registers)

options:
  -h, --help    show this help message and exit
  -s, --simple  skip dereference.
```

### Examples

```gdb
registers
registers $eax $eip $esp
```

## syscall-args

Get the syscall name and arguments based on the register values in the current state.


### Syntax

```text
usage: syscall-args [-h] [SYSCALL_NUM]

positional arguments:
  SYSCALL_NUM  syscall number to search.

options:
  -h, --help   show this help message and exit
```

# 01-b. Debugging Support - Breakpoint
## break-if-not-taken

Set a breakpoint which breaks if branch is not taken.


### Syntax

```text
usage: break-if-not-taken [-h] [--hw] LOCATION

positional arguments:
  LOCATION    the address to set breakpoint.

options:
  -h, --help  show this help message and exit
  --hw        use hardware breakpoint.
```

## break-if-taken

Set a breakpoint which breaks if branch is taken.


### Syntax

```text
usage: break-if-taken [-h] [--hw] LOCATION

positional arguments:
  LOCATION    the address to set breakpoint.

options:
  -h, --help  show this help message and exit
  --hw        use hardware breakpoint.
```

## break-rva

Set a breakpoint at relative offset from codebase.

- Alias: `brva`

### Syntax

```text
usage: break-rva [-h] OFFSET

positional arguments:
  OFFSET      the offset from codebase to set a breakpoint.

options:
  -h, --help  show this help message and exit
```

## command-break

Set a breakpoint which executes user-defined command silently and continue, if hit.


### Syntax

```text
usage: command-break [-h] [LOCATION] COMMAND

positional arguments:
  LOCATION    the address to set a breakpoint. (default: current_arch.pc)
  COMMAND     the command executed if breakpoint is hit.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
command-break 0x55555555aab9 "hexdump -n $sp+0x120"
```

## entry-break

Try to find best entry point and set a temporary breakpoint on it.

- Alias: `start`

### Syntax

```text
usage: entry-break
```

## load-break

Break if something is loaded (wrapper of `set stop-on-solib-events 1`).


### Syntax

```text
usage: load-break [-h]

options:
  -h, --help  show this help message and exit
```

## main-break

Set a breakpoint at the beginning of main with or without symbols, then continue.


### Syntax

```text
usage: main-break
```

## multi-break

Set multiple breakpoints easily.


### Syntax

```text
usage: multi-break LOCATION [LOCATION ...]

positional arguments:
  LOCATION  the address(es) to set breakpoint.
```

### Notes

```text
This command is intended to improve the readability of history
by allowing you to set multiple breakpoints on a single line.
```

## regdump-break

Set a breakpoint which dumps registers silently and continue, if hit.


### Syntax

```text
usage: regdump-break [-h] [-t TAG] [-r REGS] [LOCATION]

positional arguments:
  LOCATION         the address to set a breakpoint. (default: current_arch.pc)

options:
  -h, --help       show this help message and exit
  -t, --tag TAG    the tag if breakpoint is hit.
  -r, --regs REGS  the register name dumped if breakpoint is hit.
```

### Examples

```gdb
regdump-break 0x55555555aab9 -r rax
regdump-break 0x55555555aab9 -t "state changed" -r rax
```

# 01-c. Debugging Support - Basic Command Extension
## continue-for-qemu-user

`c` wrapper to resolve the Ctrl+C problem for qemu-user or Intel Pin.


### Syntax

```text
usage: continue-for-qemu-user [-h] [ARGS ...]

positional arguments:
  ARGS        An array of arguments to pass as is to the continue command. (default: None)

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Only when qemu-user or pin, the `c` command is redirected to `continue-for-qemu-user`.
This setting is done only once, when hook_stop_handler is called for the first time.
Nested `c` command causes a problem, so in that case gef executes the original continue command instead.
Internally, SIGINT is monitored in a forked child process (default) or another thread.
```

## down

`down` wrapper.


### Syntax

```text
usage: down [-h] [N]

positional arguments:
  N           Number of frames to move. (default: 1)

options:
  -h, --help  show this help message and exit
```

## multi-line

Execute multiple GDB commands in sequence.

- Alias: `ml`

### Syntax

```text
usage: multi-line [-h] GDB_CMD; [GDB_CMD; ...]

positional arguments:
  GDB_CMD;    semicolon-separated gdb command.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
multi-line x/4xg $rax; x/4xg $rbx
multi-line x/4xg $rax; -; x/4xg $rbx         # `-`:   newline separator
multi-line x/4xg $rax; --; x/4xg $rbx        # `--`:  bold white line (`-`) separator
multi-line x/4xg $rax; ---; x/4xg $rbx       # `---`: bold white line (`=`) separator
multi-line x/4xg $rax; -t TAG; x/4xg $rbx    # `-t TAG`:   newline separator with TAG
multi-line x/4xg $rax; --t TAG; x/4xg $rbx   # `--t TAG`:  bold white line (`-`) separator with TAG
multi-line x/4xg $rax; ---t TAG; x/4xg $rbx  # `---t TAG`: bold white line (`=`) separator with TAG
```

## nexti-for-qemu-user

`ni` wrapper for some specific architectures (OpenRISC 1000 and CRIS).


### Syntax

```text
usage: nexti-for-qemu-user [-h] [ARGS ...]

positional arguments:
  ARGS        An array of arguments to pass as is to the nexti command. (default: None)

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Only when qemu-user with specific architecture, the `ni` command is redirected to `nexti-for-qemu-user`.
This setting is done only once, when `hook_stop_handler` is called for the first time.

Target architecture:
  OpenRISC 1000: branch operations don't work well, so GEF uses breakpoints to simulate.
  CRIS: si/ni commands don't work well. so GEF uses breakpoints to simulate.
```

## stepi-for-kgdb

`si` wrapper for AArch64 KGDB that avoids stepping into pending IRQ handlers.


### Syntax

```text
usage: stepi-for-kgdb [-h]

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Only for AArch64 + kgdb.
Temporarily masks IRQ before `stepi`, then restores the original state
unless the stepped instruction intentionally modified DAIF.I.
```

## stepi-for-qemu-user

`si` wrapper for some specific architectures (OpenRISC 1000 and CRIS).


### Syntax

```text
usage: stepi-for-qemu-user [-h] [ARGS ...]

positional arguments:
  ARGS        An array of arguments to pass as is to the stepi command. (default: None)

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Only when qemu-user with specific architecture, the `si` command is redirected to `stepi-for-qemu-user`.
This setting is done only once, when `hook_stop_handler` is called for the first time.

Target architecture:
  OpenRISC 1000: branch operations don't work well, so GEF uses breakpoints to simulate.
  CRIS: si/ni commands don't work well. so GEF uses breakpoints to simulate.
```

## time

Measure the time of the GDB command.


### Syntax

```text
usage: time [-h] GDB_CMD [ARG ...]

positional arguments:
  GDB_CMD     gdb command.
  ARG         arguments of gdb command.

options:
  -h, --help  show this help message and exit
```

## up

`up` wrapper.


### Syntax

```text
usage: up [-h] [N]

positional arguments:
  N           Number of frames to move. (default: 1)

options:
  -h, --help  show this help message and exit
```

# 01-d. Debugging Support - Execution
## call-trace

Trace call, ret, and syscall using exec-until.


### Syntax

```text
usage: call-trace [-h] [-a] [-s] [-N]

options:
  -h, --help            show this help message and exit
  -a, --print-args      dump arguments, return value, and syscall args.
  -s, --syscall-only    trace syscall only.
  -N, --no-file-output  disable writing trace output to a file.
```

## exec-until

The base command to execute until specific condition.


### Syntax

```text
usage: exec-until [-h] {call,jmp,syscall,ret,all-branch,indirect-branch,memaccess,keyword,cond,user-code,libc-code,secure-world,region-change} ...

options:
  -h, --help            show this help message and exit

command:
  {call,jmp,syscall,ret,all-branch,indirect-branch,memaccess,keyword,cond,user-code,libc-code,secure-world,region-change}
```

### Examples

```gdb
exec-until call                                 # execute until call instruction
exec-until jmp                                  # execute until jmp instruction
exec-until syscall                              # execute until syscall instruction
exec-until ret                                  # execute until ret instruction
exec-until all-branch                           # execute until call/jmp/ret instruction
exec-until indirect-branch                      # execute until indirect branch instruction (x64/x86 only)
exec-until memaccess                            # execute until '[' is included by the instruction
exec-until keyword "call +r[ab]x"               # execute until specified keyword (regex)
exec-until cond "$rax==0xdead && $rbx==0xcafe"  # execute until specified condition is filled
exec-until user-code                            # execute until user code
exec-until libc-code                            # execute until libc code
exec-until secure-world                         # execute until secure world (ARM/ARM64 only)
exec-until region-change                        # execute until different region (e.g., binary itself -> libc)
```

## exec-until all-branch

Execute until call/jump/ret instruction.

- Alias: `next-all-branch`

### Syntax

```text
usage: exec-until all-branch [-h] [-I] [-n] [-N] [-e EXCLUDE] [-t | -T]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
  -t, --only-taken      break only if jump will be taken.
  -T, --only-not-taken  break only if jump will be not taken.
```

## exec-until call

Execute until call instruction.

- Alias: `next-call`

### Syntax

```text
usage: exec-until call [-h] [-I] [-n] [-N] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until cond

Execute until specified condition is filled.

- Alias: `next-cond`

### Syntax

```text
usage: exec-until cond [-h] [-I] [-n] [-N] [-e EXCLUDE] CONDITION

positional arguments:
  CONDITION             filter by condition.

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

### Examples

```gdb
exec-until cond "$rax==0xdead && $rbx==0xcafe"  # execute until specified condition is filled
exec-until cond "*(int*)$rbx==0x12"             # memory access is supported
exec-until cond "$ALL_REG==0x34"                # compare with all regs. e.g., `($rax==0x34||$rbx==0x34||...)`
```

## exec-until indirect-branch

Execute until indirect call/jmp instruction (x64/x86 only).

- Alias: `next-indirect-branch`

### Syntax

```text
usage: exec-until indirect-branch [-h] [-I] [-n] [-N] [-e EXCLUDE] [-t | -T]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
  -t, --only-taken      break only if jump will be taken.
  -T, --only-not-taken  break only if jump will be not taken.
```

## exec-until jmp

Execute until jmp instruction.

- Alias: `next-jmp`

### Syntax

```text
usage: exec-until jmp [-h] [-I] [-n] [-N] [-e EXCLUDE] [-t | -T]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
  -t, --only-taken      break only if jump will be taken.
  -T, --only-not-taken  break only if jump will be not taken.
```

## exec-until keyword

Execute until specified keyword instruction.

- Alias: `next-keyword`

### Syntax

```text
usage: exec-until keyword [-h] [-I] [-n] [-N] [-e EXCLUDE] KEYWORD [KEYWORD ...]

positional arguments:
  KEYWORD               filter by specified regex keyword.

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

### Examples

```gdb
exec-until keyword "call +r[ab]x"                         # execute until specified keyword
exec-until keyword "(push|pop) +(r[a-d]x|r[ds]i|r[sb]p)"  # another example
exec-until keyword "mov +rax, QWORD PTR \\["              # another example (need double escape)
```

## exec-until libc-code

Execute until instruction in libc code.

- Alias: `next-libc-code`

### Syntax

```text
usage: exec-until libc-code [-h] [-I] [-n] [-N] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until memaccess

Execute until memory access instruction.

- Alias: `next-mem`

### Syntax

```text
usage: exec-until memaccess [-h] [-I] [-n] [-N] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until region-change

Execute until different region.

- Alias: `next-region-change`

### Syntax

```text
usage: exec-until region-change [-h] [-I] [-n] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until ret

Execute until ret instruction.

- Alias: `next-ret`

### Syntax

```text
usage: exec-until ret [-h] [-I] [-n] [-N] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until secure-world

Execute until instruction in the secure-world (ARM/ARM64 only).

- Alias: `next-secure-world`

### Syntax

```text
usage: exec-until secure-world [-h] [-I] [-n] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until syscall

Execute until syscall instruction.

- Alias: `next-syscall`

### Syntax

```text
usage: exec-until syscall [-h] [-I] [-n] [-N] [-f FILTER] [-i IGNORE] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -f, --filter FILTER   filter by specified syscall.
  -i, --ignore IGNORE   ignore specified syscall.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## exec-until user-code

Execute until instruction in user-code.

- Alias: `next-user-code`

### Syntax

```text
usage: exec-until user-code [-h] [-I] [-n] [-N] [-e EXCLUDE]

options:
  -h, --help            show this help message and exit
  -I, --print-insn      print each instruction during execution.
  -n, --use-ni          use `ni` instead of `si`.
  -N, --skip-lib        use `ni` instead of `si` if instruction is `call xxx@plt`.
  -e, --exclude EXCLUDE
                        the address to exclude from breakpoints.
```

## xskip

Skip instructions easily.


### Syntax

```text
usage: xskip [-h] [count]

positional arguments:
  count       the count to skip.

options:
  -h, --help  show this help message and exit
```

## xuntil

Execute until specified address easily.

- Alias: `exec-next`, `stepover`, `until-next`

### Syntax

```text
usage: xuntil [-h] [--from-wrapper] [ADDRESS]

positional arguments:
  ADDRESS         the address to stop.

options:
  -h, --help      show this help message and exit
  --from-wrapper  [FOR DEVELOPER] used internally in gef, please don't use it.
```

# 01-e. Debugging Support - Assemble
## asm

Assemble inline code using Keystone.


### Syntax

```text
usage: asm [-h] [-a ARCH] [-m MODE] [-e] [-s] [-l LOCATION] [-H] INSTRUCTION [INSTRUCTION ...]

positional arguments:
  INSTRUCTION  the code to assemble.

options:
  -h, --help   show this help message and exit
  -a ARCH      specify the architecture. (default: current_arch.arch)
  -m MODE      specify the mode. (default: current_arch.mode)
  -e           use big-endian.
  -s           output like shellcode style.
  -l LOCATION  write to memory address.
  -H, --hex    show in hex style.
```

### Examples

```gdb
asm -a X86 -m 64 "mov rax, qword ptr [rax] ; inc rax ;"
asm -a X86 -m 32 "mov eax, dword ptr [eax] ; inc eax ;"
asm -a X86 -m 16 "mov ax, word ptr [ax] ; inc ax"
asm -a ARM -m ARM      "sub r1, r2, r3"
asm -a ARM -m ARM -e   "sub r1, r2, r3"
asm -a ARM -m THUMB    "movs r4, #0xf0"
asm -a ARM -m THUMB -e "movs r4, #0xf0"
asm -a ARM64 -m ARM    "ldr w1, [sp, #0x8]"
asm -a MIPS -m 32    "and $9, $6, $7"
asm -a MIPS -m 32 -e "and $9, $6, $7"
asm -a MIPS -m 64    "and $9, $6, $7"
asm -a MIPS -m 64 -e "and $9, $6, $7"
asm -a PPC -m 32 -e "add 1, 2, 3"
asm -a PPC -m 64    "add 1, 2, 3"
asm -a PPC -m 64 -e "add 1, 2, 3"
asm -a SPARC -m 32 -e "add %g1, %g2, %g3"
asm -a SPARC -m 32PLUS -e "add %g1, %g2, %g3"
asm -a SPARC -m 64 -e "add %g1, %g2, %g3"
asm -a S390X -m 64 -e "a %r0, 4095(%r15,%r1)"
```

## asm-list

List general instructions by capstone (x64/x86 only).


### Syntax

```text
usage: asm-list [-h] [-a ARCH] [-m MODE] [-e] [-b NBYTE] [-f INCLUDE] [-v EXCLUDE] [-n]

options:
  -h, --help      show this help message and exit
  -a ARCH         specify the architecture. (default: current_arch.arch)
  -m MODE         specify the mode. (default: current_arch.mode)
  -e              use big-endian.
  -b NBYTE        filter by the length of asm byte.
  -f INCLUDE      filter by specified string.
  -v EXCLUDE      filter by specified string.
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
asm-list -a X86 -m 64
asm-list -a X86 -m 32
asm-list -a X86 -m 16
```

### Notes

```text
- F0 (LOCK prefix) is ignored
- F2/F3 (REPNE/REP prefix) are ignored
- 2E/36/3E/26/64/65 (CS/SS/DS/ES/FS/GS override prefix) are ignored
- 2E/3E (branch hint prefix) are ignored
- 66 (operand size prefix) is included
- 67 (address size prefix) is ignored
- 40-4F (REX prefix) are ignored
- C4/C5 (VEX prefix) are ignored
- 8F (XOP prefix) is ignored
- 62 (EVEX prefix) is ignored
```

## capstone-disassemble

Use capstone disassembly framework to disassemble code.

- Alias: `cs-dis`, `pdisas`, `nearpc`

### Syntax

```text
usage: capstone-disassemble [-h] [-l LENGTH] [LOCATION] [ARGS ...]

positional arguments:
  LOCATION             the address to disassemble. (default: current_arch.pc)
  ARGS                 arguments for capstone. see following example.

options:
  -h, --help           show this help message and exit
  -l, --length LENGTH  the length to disassemble. (default: context.nb_lines_code)
```

### Examples

```gdb
capstone-disassemble -l 50 $pc                             # dump from $pc up to 50 lines later
capstone-disassemble -l 50 $pc arch=ARM mode=ARM endian=1  # specify arch, mode and endian (1:big endian)
```

### Notes

```text
Available architectures and modes:
 - ARM      ARM / THUMB
 - ARM64    ARM
 - MIPS     32 / 64
 - PPC      32 / 64
 - SPARC    32 / 32PLUS / 64
 - X86      16 / 32 / 64
```

## dasm

Disassemble inline code using Capstone.


### Syntax

```text
usage: dasm [-h] [-a ARCH] [-m MODE] [-e] HEX_CODE [HEX_CODE ...]

positional arguments:
  HEX_CODE    the hex code to disassemble.

options:
  -h, --help  show this help message and exit
  -a ARCH     specify the architecture. (default: current_arch.arch)
  -m MODE     specify the mode. (default: current_arch.mode)
  -e          use big-endian.
```

### Examples

```gdb
dasm -a X86 -m 64 "488b00 48ffc0"
dasm -a X86 -m 32 "8b00 40"
dasm -a X86 -m 16 "8b00 40"
dasm -a ARM -m ARM      "031042e0"
dasm -a ARM -m ARM -e   "e0421003"
dasm -a ARM -m THUMB    "f024"
dasm -a ARM -m THUMB -e "24f0"
dasm -a ARM64 -m ARM    "e10b40b9"
dasm -a MIPS -m 32    "2448c700"
dasm -a MIPS -m 32 -e "00c74824"
dasm -a MIPS -m 64    "2448c700"
dasm -a MIPS -m 64 -e "00c74824"
dasm -a PPC -m 32 -e "7c221a14"
dasm -a PPC -m 64    "141a227c"
dasm -a PPC -m 64 -e "7c221a14"
dasm -a SPARC -m 32 -e "86004002"
dasm -a SPARC -m 32PLUS -e "86004002"
dasm -a SPARC -m 64 -e "86004002"
dasm -a RISCV -m 32 "97c10600"
dasm -a RISCV -m 64 "97c10600"
dasm -a S390X -m 64 -e "5a0f1fff"
dasm -a M68K -m 32 -e "9dce"
dasm -a LOONGARCH -m 64 "89001500" # capstone v6.x~
dasm -a LOONGARCH -m 32 "89001500" # capstone v6.x~
dasm -a ALPHA -m 64    "0b00bd27" # capstone v6.x~
dasm -a ALPHA -m 64 -e "27bd000b" # capstone v6.x~
dasm -a HPPA -m 32 -e "0fc01299" # capstone v6.x~
dasm -a HPPA -m 64 -e "0fc01299" # capstone v6.x~
```

## ii

Shortcut `x/50i $pc` with opcode bytes.


### Syntax

```text
usage: ii [-h] [-l LENGTH] [LOCATION]

positional arguments:
  LOCATION             the dump start address.

options:
  -h, --help           show this help message and exit
  -l, --length LENGTH  the dump instruction length.
```

# 01-f. Debugging Support - Context Extension
## comment

The base command to add, remove, list or clear the comment.


### Syntax

```text
usage: comment [-h] {add,remove,list,clear} ...

options:
  -h, --help            show this help message and exit

command:
  {add,remove,list,clear}
```

### Notes

```text
Comments are temporary only. Note that it will be deleted when GDB exits.
```

## comment add

Add a comment to specific address.


### Syntax

```text
usage: comment add [-h] LOCATION COMMENT

positional arguments:
  LOCATION    the address for comment.
  COMMENT     the comment to print when hit.

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Comments are temporary only. Note that it will be deleted when GDB exits.
```

## comment clear

Clear all comments.


### Syntax

```text
usage: comment clear [-h]

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Comments are temporary only. Note that it will be deleted when GDB exits.
```

## comment list

List the comments.


### Syntax

```text
usage: comment list [-h]

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Comments are temporary only. Note that it will be deleted when GDB exits.
```

## comment remove

Remove the specified comment.


### Syntax

```text
usage: comment remove [-h] LOCATION [INDEX]

positional arguments:
  LOCATION    the address for comment.
  INDEX       the index of comment to remove. If omitted, all comments for that address will be deleted.

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Comments are temporary only. Note that it will be deleted when GDB exits.
```

## extra

The base command to add, remove, list or clear user specified command to `context extra`.


### Syntax

```text
usage: extra [-h] {add,remove,list,clear} ...

options:
  -h, --help            show this help message and exit

command:
  {add,remove,list,clear}
```

## extra add

Add user specified command to execute when each step.


### Syntax

```text
usage: extra add [-h] CMD [CMD ...]

positional arguments:
  CMD         the command to execute when each step.

options:
  -h, --help  show this help message and exit
```

## extra clear

Clear all user specified commands to execute when each step.


### Syntax

```text
usage: extra clear [-h]

options:
  -h, --help  show this help message and exit
```

## extra list

List user specified command to execute when each step.


### Syntax

```text
usage: extra list [-h]

options:
  -h, --help  show this help message and exit
```

## extra remove

Remove user specified command to execute when each step.


### Syntax

```text
usage: extra remove [-h] INDEX

positional arguments:
  INDEX       the index of command to remove from automatically execution each step.

options:
  -h, --help  show this help message and exit
```

## highlight

The base command to highlight user-defined text matches, which modifies GEF output universally.


### Syntax

```text
usage: highlight [-h] {add,remove,list,clear} ...

options:
  -h, --help            show this help message and exit

command:
  {add,remove,list,clear}
```

## highlight add

Add a match to the highlight table.


### Syntax

```text
usage: highlight add [-h] MATCH COLOR [COLOR ...]

positional arguments:
  MATCH       the keyword phrase to highlight.
  COLOR       the color used to highlight.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
highlight add "call   rcx" bold yellow
```

### Notes

```text
use config `gef config highlight.regex true` if need regex.
```

## highlight clear

Clear the highlight table.


### Syntax

```text
usage: highlight clear [-h]

options:
  -h, --help  show this help message and exit
```

## highlight list

Display the current highlight table with matches to colors.


### Syntax

```text
usage: highlight list [-h]

options:
  -h, --help  show this help message and exit
```

## highlight remove

Remove a match in the highlight table.


### Syntax

```text
usage: highlight remove [-h] MATCH

positional arguments:
  MATCH       the keyword phrase to remove from highlight.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
highlight remove "call   rcx"
```

## memory

The base command to watch the memory.


### Syntax

```text
usage: memory [-h] {watch,unwatch,reset,list} ...

options:
  -h, --help            show this help message and exit

command:
  {watch,unwatch,reset,list}
```

## memory list

List all watchpoints to display in context layout.


### Syntax

```text
usage: memory list [-h]

options:
  -h, --help  show this help message and exit
```

## memory reset

Remove all watchpoints.


### Syntax

```text
usage: memory reset [-h]

options:
  -h, --help  show this help message and exit
```

## memory unwatch

Remove address ranges from the memory view.


### Syntax

```text
usage: memory unwatch [-h] ADDRESS

positional arguments:
  ADDRESS     the memory address to deregister for display in `context memory`.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
memory unwatch 0x603000
memory unwatch $sp
```

## memory watch

Add address ranges to the memory view.


### Syntax

```text
usage: memory watch [-h] ADDRESS [COUNT] [{byte,word,dword,qword,pointers}]

positional arguments:
  ADDRESS               the memory address to register for display in `context memory`.
  COUNT                 the count of displayed units. (default: 16)
  {byte,word,dword,qword,pointers}
                        the size of unit. (default: pointers)

options:
  -h, --help            show this help message and exit
```

### Examples

```gdb
memory watch 0x603000 0x100 byte
memory watch $sp
```

## smart-cpp-function-name

Toggle the setting of `context.smart_cpp_function_name`.

- Alias: `cpp`

### Syntax

```text
usage: smart-cpp-function-name [-h]

options:
  -h, --help  show this help message and exit
```

# 01-g. Debugging Support - Syscall
## call-syscall

A wrapper for calling syscall easily.


### Syntax

```text
usage: call-syscall [-h] SYSCALL_NAME [SYSCALL_ARG ...]

positional arguments:
  SYSCALL_NAME  system call name to invoke.
  SYSCALL_ARG   arguments of system call.

options:
  -h, --help    show this help message and exit
```

### Examples

```gdb
call-syscall write 1 "*(void**)($rsp+0x18)" 15
```

## hijack-fd

Redirect the file descriptor during execution.


### Syntax

```text
usage: hijack-fd [-h] [--fd-adjust-connect FD_ADJUST_CONNECT] [--fd-adjust-dup3 FD_ADJUST_DUP3] [-q] OLD_FD NEW_OUTPUT

positional arguments:
  OLD_FD                file descriptor number to redirect.
  NEW_OUTPUT            the location redirected data is stored.

options:
  -h, --help            show this help message and exit
  --fd-adjust-connect FD_ADJUST_CONNECT
                        slide value when `connect` syscall result and the actual opened FD differ (for old qemu-user).
  --fd-adjust-dup3 FD_ADJUST_DUP3
                        slide value when `dup3` syscall result and the actual opened FD differ (for old qemu-user).
  -q, --quiet           quiet execution.
```

### Examples

```gdb
hijack-fd 2 /tmp/gef/stderr.txt
hijack-fd 2 localhost:8000  # determined as the socket by the presence of `:`.
```

## killthreads

Invoke pthread_exit(0) for a specific THREAD_ID.


### Syntax

```text
usage: killthreads [-h] [-a] [-e EXCLUDE] [-c] [THREAD_ID ...]

positional arguments:
  THREAD_ID             the thread id (not TID) to kill.

options:
  -h, --help            show this help message and exit
  -a, --all             kill all threads except current thread.
  -e, --exclude EXCLUDE
                        the thread id not to kill.
  -c, --commit          commit to kill.
```

### Examples

```gdb
killthreads 2 3   # kill threads that `Thread Id` is 2 or 3
```

## mmap

Allocate a new memory.


### Syntax

```text
usage: mmap [-h] [LOCATION] [SIZE] [PERMISSION]

positional arguments:
  LOCATION    the address to allocate. (default: None)
  SIZE        the size to allocate. (default: 4096)
  PERMISSION  the permission to allocate. `_` is interpreted as `-`. (default: rwx)

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
mmap 0x10000 0x1000 r-x
mmap 0 0x1000 _wx        # '_' means '-'
```

## mprotect

Change a page permission (default: RWX).


### Syntax

```text
usage: mprotect [-h] [-s SIZE] LOCATION [PERMISSION]

positional arguments:
  LOCATION         the address to change the permission.
  PERMISSION       the permission you set to the LOCATION. (default: rwx)

options:
  -h, --help       show this help message and exit
  -s, --size SIZE  the size to change the permission (0x1000 align).
```

### Examples

```gdb
mprotect $sp rwx
mprotect 0x7ffff7e1b000 ___           # '_' means '-'
mprotect 0x7ffff7e1b000 ___ -s 0x1000 # change only first 0x1000 bytes
```

### Notes

```text
By default, the permissions will be changed for the entire map including the specified address.
If a size is specified, the permissions will only be changed for the range of the specified address up to the size.
```

## munmap

Unmap a mapped memory.


### Syntax

```text
usage: munmap [-h] LOCATION [SIZE]

positional arguments:
  LOCATION    the address to unmap.
  SIZE        the size to unmap.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
munmap $sp                    # unmap whole stack area
munmap 0x7ffffffde000 0x1000  # unmap specified area
```

### Notes

```text
By default, the entire map containing the specified address is freed.
If a size is specified, the area from the specified address to that size will be unmapped.
```

## syscall-search

Search for the syscall number for a specified architecture.

- Alias: `ss`

### Syntax

```text
usage: syscall-search [-h] [-a ARCH] [-m MODE] [-n] [-v] [SYSCALL_NAME|SYSCALL_NUM]

positional arguments:
  SYSCALL_NAME|SYSCALL_NUM
                        syscall name or number to search. Regex is available.

options:
  -h, --help            show this help message and exit
  -a ARCH               specify the architecture. (default: current_arch.arch)
  -m MODE               specify the mode. (default: current_arch.mode)
  -n, --no-pager        do not use the pager.
  -v, --verbose         display prototype of syscall.
```

### Examples

```gdb
syscall-search -a X86 -m 64       "^writev?"  # amd64
syscall-search -a X86 -m 32       "^writev?"  # i386 on amd64
syscall-search -a X86 -m N32      "^writev?"  # i386 native
syscall-search -a X86 -m x32      "^writev?"  # x32 mode
syscall-search -a ARM64 -m ARM    "^writev?"  # arm64
syscall-search -a ARM -m 32       "^writev?"  # arm32 on arm64
syscall-search -a ARM -m N32      "^writev?"  # arm32 native
syscall-search -a MIPS -m 32      "^writev?"  # mips32
syscall-search -a MIPS -m n32     "^writev?"  # mipsn32
syscall-search -a MIPS -m 64      "^writev?"  # mips64
syscall-search -a PPC -m 32       "^writev?"  # ppc32
syscall-search -a PPC -m 64       "^writev?"  # ppc64
syscall-search -a SPARC -m 32     "^writev?"  # sparc32
syscall-search -a SPARC -m 32PLUS "^writev?"  # sparc32plus
syscall-search -a SPARC -m 64     "^writev?"  # sparc64
syscall-search -a RISCV -m 32     "^writev?"  # riscv32
syscall-search -a RISCV -m 64     "^writev?"  # riscv64
syscall-search -a S390X           "^writev?"  # s390x
syscall-search -a SH4             "^writev?"  # sh4
syscall-search -a M68K -m 32      "^writev?"  # m68k
syscall-search -a ALPHA           "^writev?"  # alpha
syscall-search -a HPPA -m 32      "^writev?"  # hppa32
syscall-search -a HPPA -m 64      "^writev?"  # hppa64
syscall-search -a OR1K            "^writev?"  # or1k
syscall-search -a NIOS2           "^writev?"  # nios2
syscall-search -a MICROBLAZE      "^writev?"  # microblaze
syscall-search -a XTENSA          "^writev?"  # xtensa
syscall-search -a CRIS            "^writev?"  # cris
syscall-search -a LOONGARCH -m 64 "^writev?"  # loongarch64
syscall-search -a ARC -m 32       "^writev?"  # arc32
syscall-search -a ARC -m 64       "^writev?"  # arc64
syscall-search -a CSKY            "^writev?"  # csky
```

## xtap

Tap read/write syscalls on specific file descriptors and hexdump the transferred data.


### Syntax

```text
usage: xtap [-h] [--max MAXLEN] FD [FD ...]

positional arguments:
  FD            the file descriptor(s) to tap.

options:
  -h, --help    show this help message and exit
  --max MAXLEN  limit the number of bytes to hexdump per transfer.
```

### Examples

```gdb
xtap 0               # tap stdin
xtap 4               # tap fd 4 (e.g. a socket)
xtap 0 1 2           # tap stdin/stdout/stderr
xtap 4 --max 0x40    # tap fd 4, dump at most 0x40 bytes per transfer
```

### Notes

```text
Hooked syscalls:
  read-like: read, recvfrom, recvmsg, recvmmsg, recvmmsg_time64, pread64, preadv, preadv2, readv
  write-like: write, sendto, sendmsg, sendmmsg, pwrite64, pwritev, pwritev2, writev

- Relies on `catch syscall`.
- Auto-continues; stops on a user breakpoint or Ctrl+C.
- qemu-user is unsupported: its gdbstub does not update the return-value register
  at syscall-return, so read-like sizes are wrong. Use a native target.
```

# 01-h. Debugging Support - Emulation
## angr

Use angr to find simple constraints.


### Syntax

```text
usage: angr [-h] [-f FIND] [-a AVOID] [-s LOCATION SIZE] [-t TYPE] [-S] [-H]

options:
  -h, --help            show this help message and exit
  -f, --find FIND       to find addresses.
  -a, --avoid AVOID     to avoid addresses.
  -s, --sym LOCATION SIZE
                        make memory symbolic.
  -t, --type TYPE       symbolic variable type. (A:A-Z, a:a-z, 0:0-9, s:0x20-0x7e, ?:0x00-0xff, z:0x00)
  -S, --skip-execution  do not execute.
  -H, --hook-stack-chk-fail-by-direct-return
                        hook `__stack_chk_fail@plt` by just `return`.
```

### Examples

```gdb
angr -f 0x400607 -a 0x400613 -s $rdi 30
angr -f 0x400607 -a 0x400613 -s $rdi 30 -t Aa0                 # sym0:[A-Za-z0-9]+
angr -f 0x400607 -a 0x400613 -s $rdi 30 -t ? -s $rdx 20 -t Az  # sym0:[0x00-0xff]+, sym1:[A-Z\0]+
```

### Notes

```text
If there is a stack canary check, angr may fail to find the solution.
This occurs when execution begins inside a function but terminates outside of it.
To avoid it, you need to replace these instructions (e.g., `sub rdx, fs:28h; jnz loc_XXX`) with `nop`s.
Please patch memory or make other appropriate modifications before running the `angr` command.

The -H option is designed to handle this issue automatically.
But it assumes that there is a `ret` after `call __stack_chk_fail@plt`.
Note that it will fail if there is a `ret` before `call __stack_chk_fail@plt`.
```

## unicorn-emulate

Use Unicorn-Engine to emulate the behavior of the binary.

- Alias: `emulate`

### Syntax

```text
usage: unicorn-emulate [-h] [-f FROM_LOCATION] [-g NB_GADGET | -t TO_LOCATION | -n NB_INSN] [-i] [-s] [-v] [-S] [-A] [-E] [-I] [-q]

options:
  -h, --help            show this help message and exit
  -f, --from-location FROM_LOCATION
                        specifies the start address of the emulated run. (default: current_arch.pc)
  -g, --nb-gadget NB_GADGET
                        the number of gadgets to execute. (default mode, NB_GADGET: 10)
  -t, --to-location TO_LOCATION
                        the end address of the emulated run.
  -n, --nb-insn NB_INSN
                        the number of instructions from `FROM_LOCATION`.
  -i, --only-insns      show only instructions (no registers, memories, etc).
  -s, --skip-emulation, --save
                        do not run, just save the script.
  -v, --verbose         displays the register values for each executed instruction.
  -S, --add-sse         initialization and display XMM registers (x64/x86 only).
  -A, --avoid-avx-neon-opt-func
                        patch GOT to replace (e.g., __XXX_avx2 with XXX), as Unicorn does not support them.
  -E, --emulate-mmap    [FOR DEVELOPER] used internally in gef, please don't use it.
  -I, --emulate-insn    [FOR DEVELOPER] used internally in gef, please don't use it.
  -q, --quiet           quiet execution.
```

### Examples

```gdb
unicorn-emulate -g 10               # from $pc to the point where 4 instructions are executed
unicorn-emulate -n 5                # from $pc to 5 later instructions (assume it is no branch)
unicorn-emulate -t 0x805678a4 -s    # from $pc to specified address with saving script
```

### Notes

```text
unicorn does not support emulating syscall.
unicorn does not support some instructions. (e.g., xsavec, xrstor, vpbroadcastb, vldr, etc.)
unicorn does not emulate ARM kernel-provided-user-helpers like $pc=0xffff0fe0, 0xffff0fc0, etc.
see: https://www.kernel.org/doc/Documentation/arm/kernel_user_helpers.txt
```

# 01-i. Debugging Support - Other
## add-symbol-temporary

Add symbol from command temporarily.


### Syntax

```text
usage: add-symbol-temporary [-h] [-q] FUNCTION_NAME START_ADDR [END_ADDR]

positional arguments:
  FUNCTION_NAME  new symbol name to add.
  START_ADDR     start address to add a symbol.
  END_ADDR       end address to add a symbol.

options:
  -h, --help     show this help message and exit
  -q, --quiet    enable quiet mode.
```

### Examples

```gdb
add-symbol-temporary your_func_name $rip $rip+0x20
```

## follow

View / modify the follow-fork-mode setting of GDB.


### Syntax

```text
usage: follow [-h] [{child,parent}]

positional arguments:
  {child,parent}  set gdb follow settings.

options:
  -h, --help      show this help message and exit
```

## format-string-helper

The helper to search for exploitable format strings.

- Alias: `fmtstr-helper`

### Syntax

```text
usage: format-string-helper [-h] [-r] [-v]

options:
  -h, --help            show this help message and exit
  -r, --remove-breakpoint
                        remove the format-string-helper related breakpoints.
  -v, --verbose         display target functions of breakpoint.
```

## onegadget

Invoke `one_gadget`.


### Syntax

```text
usage: onegadget [-h] [-s]

options:
  -h, --help            show this help message and exit
  -s, --apply-smart-filter
                        filter valid gadgets for the current register and memory values (x64 only).
```

## ropper

Invoke ropper to search rop gadgets.


### Syntax

```text
usage: ropper [-h] [ROPPER_OPTIONS ...]

positional arguments:
  ROPPER_OPTIONS  An array of arguments to pass as is to the ropper command. (default: None)

options:
  -h, --help      show this help message and exit
```

### Examples

```gdb
ropper
ropper -h                  # show detail of options
ropper --jmp "rax,rcx"     # filter by jmp registers
ropper --search "pop r?x"  # filter by pop registers
```

## rp

Invoke rp++ (v2) command to search rop gadgets (x64/x86 only).


### Syntax

```text
usage: rp [-h] (--bin | --libc | --file FILE | --kernel) [-f FILTER] [-r ROP_N] [-a] [-n] [--no-print]

options:
  -h, --help            show this help message and exit
  --bin                 apply rp++ to binary itself.
  --libc                apply rp++ to libc.so searched from vmmap.
  --file FILE           apply rp++ to specified file.
  --kernel              dump kernel, then apply vmlinux-to-elf and rp++.
  -f, --filter FILTER   REGEXP filter.
  -r, --rop ROP_N       the max length of rop gadget. (default: 3)
  -a, --allow-branches  enable --allow-branches.
  -n, --no-pager        do not use the pager.
  --no-print            run rp, create a temporary file, but don't display it.
```

### Examples

```gdb
rp --bin -f "pop r[abcd]x"
rp --libc -f "(xchg|mov) [re]sp, \\w+" -f "ret"
rp --bin -a                                      # show more gadgets
rp --kernel                                      # only under qemu-system
```

## seccomp

Invoke `ceccomp` or `seccomp-tools`.

- Alias: `ceccomp`

### Syntax

```text
usage: seccomp [-h] [-c | -s]

options:
  -h, --help            show this help message and exit
  -c, --force-ceccomp   force use ceccomp.
  -s, --force-seccomp-tools
                        force use seccomp-tools.
```

### Notes

```text
Default: Search `ceccomp` -> `seccomp-tools`, and use found one.
With `-c` or `-s`: Forces GEF to use the specified one.
```

# 02-a. Process Information - General
## elf-info

Display a limited subset of ELF header information.


### Syntax

```text
usage: elf-info [-h] [-e] [-r] [-f FILE] [-a ADDRESS] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -e, --use-readelf     use readelf.
  -r, --remote          parse remote binary if download feature is available.
  -f, --file FILE       the file path to parse.
  -a, --address ADDRESS
                        the memory address to parse.
  -n, --no-pager        do not use the pager.
  -v, --verbose         dump the content of each section.
```

### Examples

```gdb
elf-info                    # parse binary itself
elf-info -f /bin/ls         # parse binary
elf-info -f /bin/ls -r      # parse remote binary
elf-info -a 0x555555554000  # parse memory
elf-info -e -f /bin/ls      # show `readelf -a FILE | less`
```

## fds

Display opened file descriptors.


### Syntax

```text
usage: fds [-h]

options:
  -h, --help  show this help message and exit
```

## proc-dump

Dump each file under `/proc/PID`.


### Syntax

```text
usage: proc-dump [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## proc-info

Extend the info given by GDB `info proc`.

- Alias: `pr`

### Syntax

```text
usage: proc-info [-h]

options:
  -h, --help  show this help message and exit
```

## ps

Display a smart list of processes.


### Syntax

```text
usage: ps [-h] [-a ATTACH] [-n] [-v] [REGEX_PATTERN]

positional arguments:
  REGEX_PATTERN        filter by regex.

options:
  -h, --help           show this help message and exit
  -a, --attach ATTACH  attach it.
  -n, --no-pager       do not use the pager.
  -v, --verbose        include kernel thread, socat, grep, gdb, sshd, bash, systemd, etc.
```

### Examples

```gdb
ps
ps ./a.out
```

# 02-b. Process Information - Base Address
## codebase

Display various base addresses.

- Alias: `base`

### Syntax

```text
usage: codebase [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## fsbase

Display fsbase address.

- Alias: `fs`

### Syntax

```text
usage: fsbase [-h]

options:
  -h, --help  show this help message and exit
```

### Notes

```text
This command overwrites original "fs (=tui focus)" command.
```

## gsbase

Display gsbase address.

- Alias: `gs`

### Syntax

```text
usage: gsbase [-h]

options:
  -h, --help  show this help message and exit
```

## heapbase

Display heap base address.


### Syntax

```text
usage: heapbase [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## ld

Display ld base address.


### Syntax

```text
usage: ld [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## libc

Display libc base address.


### Syntax

```text
usage: libc [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## tls

Display TLS base address. Requires glibc.


### Syntax

```text
usage: tls [-h] [-a] [-i THREAD_ID] [-s] [-v] [-V] [-n]

options:
  -h, --help            show this help message and exit
  -a, --all             show all TLS address.
  -i, --thread-id THREAD_ID
                        show specific TLS address.
  -s, --symbol-hint     show hints if symbol is available (x64/x86 only).
  -v, --verbose         show more entries (+16).
  -V, --more-verbose    show more entries (+256).
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
tls -vvv  # repeat `-v` to display more lines
```

# 02-c. Process Information - Memory/Section
## vmmap

Display a comprehensive layout of the virtual memory mapping.


### Syntax

```text
usage: vmmap [-h] [--outer] [-n] [-q] [FILTER]

positional arguments:
  FILTER          filter string.

options:
  -h, --help      show this help message and exit
  --outer         display qemu-user's memory map instead of emulated process's memory map.
  -n, --no-pager  do not use the pager.
  -q, --quiet     do not display register information.
```

### Examples

```gdb
vmmap libc             # show only lines containing the string `libc`
vmmap binary           # 'binary' means the area executable itself
vmmap 0x555555577ab0   # show only lines included specified address
vmmap --outer          # show qemu-user memory map; only valid in qemu-user mode
```

## xfiles

Display all libraries (and sections) loaded by binary.


### Syntax

```text
usage: xfiles [-h] [-n] [FILTER ...]

positional arguments:
  FILTER          regex filter string.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
xfiles libc
xfiles got plt
xfiles IO_vtables
```

## xinfo

Retrieve and display runtime information for the location(s) given as parameter.


### Syntax

```text
usage: xinfo [-h] [LOCATION ...]

positional arguments:
  LOCATION    the memory address to show the information. (default: current_arch.pc)

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
xinfo $pc
```

# 02-d. Process Information - Trivial Information
## argv

Display the program's argv array.


### Syntax

```text
usage: argv [-h] [-v] [-i] [-n]

options:
  -h, --help            show this help message and exit
  -v, --verbose         print all elements. (default: outputs up to 100)
  -i, --increase-limit  increase rounding limit from 128 bytes to 4096 bytes.
  -n, --no-pager        do not use the pager.
```

## auxv

Display ELF auxiliary vectors.


### Syntax

```text
usage: auxv [-h] [-f]

options:
  -h, --help            show this help message and exit
  -f, --force-heuristic
                        use heuristic detection.
```

## dumpargs

Dump arguments of current function.

- Alias: `args`

### Syntax

```text
usage: dumpargs [-h] [-c COUNT] [-o]

options:
  -h, --help            show this help message and exit
  -c, --count COUNT     number of arguments to guess.
  -o, --out-of-function
                        assume here is out of the function.
```

## envp

Display initial envp from __environ@ld, or modified envp from last_environ@libc.


### Syntax

```text
usage: envp [-h] [-v] [-i] [-n]

options:
  -h, --help            show this help message and exit
  -v, --verbose         print all elements. (default: outputs up to 100)
  -i, --increase-limit  increase rounding limit from 128 bytes to 4096 bytes.
  -n, --no-pager        do not use the pager.
```

## errno

Convert errno (or argument) to its string representation.


### Syntax

```text
usage: errno [-h] [-a] [-n] [ERRNO]

positional arguments:
  ERRNO           show specific errno definitions.

options:
  -h, --help      show this help message and exit
  -a, --all       show all errno definitions.
  -n, --no-pager  do not use the pager.
```

## filename

Display current debugged filename.


### Syntax

```text
usage: filename [-h]

options:
  -h, --help  show this help message and exit
```

## pid

Display the local PID or remote PID.


### Syntax

```text
usage: pid [-h]

options:
  -h, --help  show this help message and exit
```

## stack-frame

Display the entire stack of the current frame.


### Syntax

```text
usage: stack-frame [-h]

options:
  -h, --help  show this help message and exit
```

## tid

Display the Thread ID.


### Syntax

```text
usage: tid [-h]

options:
  -h, --help  show this help message and exit
```

## vdso

Disassemble the text area of vdso smartly.


### Syntax

```text
usage: vdso [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## vvar

Dump the vvar area (x64/x86 only).


### Syntax

```text
usage: vvar [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

# 02-e. Process Information - Complex Structure Information
## dtor-dump

Display registered destructor functions.


### Syntax

```text
usage: dtor-dump [-h] [-r] [-f FILE] [--tdl TDL]

options:
  -h, --help       show this help message and exit
  -r, --remote     parse remote binary if download feature is available.
  -f, --file FILE  the file path to parse.
  --tdl TDL        specify the offset of `tls_dtor_list` from TLS base.
```

### Examples

```gdb
dtor-dump
dtor-dump --tdl 0x50                # specify offset of tls_dtor_list
dtor-dump --tdl 0xffffffffffffffa8  # specify negative offset
```

## dwarf-exception-handler

Dump the DWARF exception handler information with the byte code itself.


### Syntax

```text
usage: dwarf-exception-handler [-h] [-hh] [-f FILE] [-r] [-x] [-n]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -f, --file FILE     the file path to parse.
  -r, --remote        parse remote binary if download feature is available.
  -x, --hexdump       with hexdump.
  -n, --no-pager      do not use the pager.
```

### Examples

```gdb
dwarf-exception-handler                  # parse loaded binary
dwarf-exception-handler -r               # parse remote binary
dwarf-exception-handler -f /usr/bin/apt  # parse specified binary
dwarf-exception-handler -x               # with hexdump
```

### Notes

```text
Simplified DWARF exception structure:

[OLD IMPLEMENTATION]
 libgcc_s.so bss area               ELF Program Header (for .eh_frame_hdr)
+-----------------------+      +-->+----------------+
| ...                   |      |   | p_type         |
| frame_hdr_cache_head  |---+  |   | p_flags        |
+-frame_hdr_cache_entry-+<--+  |   | p_offset       |
| pc_low                |      |   | p_vaddr        |----+
| pc_high               |      |   | p_paddr        |    |
| load_base             |      |   | p_filesz       |    |
| p_eh_frame_hdr        |------+   | p_memsz        |    |
| p_dynamic             |          | p_align        |    |         [NEW IMPLEMENTATION]
| link                  |---+      +----------------+    |          _dlfo_main@ld.so rodata area
+-frame_hdr_cache_entry-+<--+                            |          _dlfo_nodelete_mappings@ld.so rodata area
| pc_low                |                                |         +-------------+
| pc_high               |                                |         | map_start   |
| load_base             |                                |         | map_end     |
| p_eh_frame_hdr        |                                |         | map         |
| p_dynamic             |                                |<--------| eh_frame    |
| link                  |                                |         | (eh_dbase)  |
+-----------------------+                                |         | (eh_count)  |
The frame_hdr_cache_head and frame_hdr_cache_entry are   |         +-------------+
initialized the first time they are called.              |
                                                         |
                           +-----------------------------+
                           |
.eh_frame_hdr              |      .eh_frame                                           .gcc_except_table
+----------------------+<--+  +-->+-CIE-------------------+<--+                   +-->+-LSDA-----------------+
| version              |      |   | length                |   |                   |   | lpstart_enc          |
| eh_frame_ptr_enc     |      |   | cie_id (=0)           |   |                   |   | ttype_enc            |
| fde_count_enc        |      |   | version               |   |                   |   | ttype_off            |
| table_enc            |      |   | augmentation_string   |   |                   |   | call_site_encoding   |
| eh_frame_ptr         |------+   | code_alignment_factor |   |                   |   | call_site_table_len  |
| fde_count            |          | data_alignment_factor |   |                   |   |+-CallSite-----------+|
| Table[0] initial_loc |          | retaddr_register      |   |                   |   || call_site_start    || try_start
| Table[0] fde         |---+      | augmentation_len      |   |                   |   || call_site_length   || try_end
| Table[1] initial_loc |   |      | augmentation_data[0]  |   |                   |   || landing_pad        || catch_start
| Table[1] fde         |   |      | ...                   |-(augmentation=='P')-+ |   || action             ||---+
| ...                  |   |      | ...                   |   |                 | |   |+-CallSite-----------+|   |
| Table[N] initial_loc |   |      | augmentation_data[N]  |   |                 | |   || ...                ||   |
| Table[N] fde         |   |      | program               |   |                 | |   |+-ActionTable--------+|<--+
+----------------------+   +----->+-FDE-------------------+   |                 | |   || ar_filter          ||---+
                                  | length                |   |                 | |   || ar_disp            ||   |
                                  | cie_pointer (!=0)     |---+                 | |   |+-ActionTable--------+|   |
                                  | pc_begin              | try_catch_base      | |   || ...                ||   |
                                  | pc_range              |                     | |   |+-TTypeTable---------+|   |
                                  | augmentation_len      |                     | |   || ...(stored upward) ||   |
                                  | augmentation_data[0]  |                     | |   |+-TTypeTable---------+|<--+
                                  | ...                   |-(augmentation=='L')-|-+   || ttype              ||---> type_info
                                  | augmentation_data[N]  |                     |     |+--------------------+|
                                  | program               |                     |     +-LSDA-----------------+
                                  +-CIE-------------------+   +-----------------+     | ...                  |
                                  | ...                   |   |                       +----------------------+
                                  +-FDE-------------------+   |
                                  | ...                   |   |
                                  +-----------------------+   |
                                                              +----> personality_routine(=__gxx_personality_v0@libstdc++.so)
```

## dynamic

Display current status of the _DYNAMIC area.


### Syntax

```text
usage: dynamic [-h] [-f FILENAME | -e ELF_ADDRESS | -d DYNAMIC_ADDRESS] [--size DYNAMIC_SIZE] [-n]

options:
  -h, --help           show this help message and exit
  -f FILENAME          the filename to parse.
  -e ELF_ADDRESS       the ELF address to parse.
  -d DYNAMIC_ADDRESS   the dynamic address to parse.
  --size DYNAMIC_SIZE  use specified size of dynamic region.
  -n, --no-pager       do not use the pager.
```

### Examples

```gdb
dynamic                                         # dump itself
dynamic -f /usr/lib/x86_64-linux-gnu/libc.so.6  # dump specified binary
dynamic -e 0x555555554000                       # dump specified address as ELF
dynamic -d 0x555555575a98                       # dump specified address as dynamic
dynamic -d 0x555555575a98 --size 0x1c0          # dump specified address with specified size
```

## fpchain

Dump chains from __IO_list_all.


### Syntax

```text
usage: fpchain [-h] [address]

positional arguments:
  address     the _IO_list_all address to parse.

options:
  -h, --help  show this help message and exit
```

## got

Display current status of the got/plt inside the process.

- Alias: `plt`

### Syntax

```text
usage: got [-h] [-f FILE] [-e ELF_ADDRESS] [-r] [-n] [-q] [-v] [--exact] [--cppfilt] [FILTER ...]

positional arguments:
  FILTER                filter string.

options:
  -h, --help            show this help message and exit
  -f, --file FILE       the filename to parse.
  -e, --elf-address ELF_ADDRESS
                        the ELF address to parse.
  -r, --remote          parse remote binary if download feature is available.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
  -v, --verbose         verbose output.
  --exact               use exact match for function name.
  --cppfilt             use c++filt to demangle.
```

### Examples

```gdb
got read print                              # filter specified keyword
got -f /usr/lib/x86_64-linux-gnu/libc.so.6  # specified target binary
got -f /bin/ls -e 0x4000000000              # use specified address, it is useful under qemu
```

## got-all

Show got entries for all libraries.


### Syntax

```text
usage: got-all [-h] [-r] [-n] [-v] [--exact] [--cppfilt] [FILTER ...]

positional arguments:
  FILTER          filter string.

options:
  -h, --help      show this help message and exit
  -r, --remote    parse remote binary if download feature is available.
  -n, --no-pager  do not use the pager.
  -v, --verbose   verbose output.
  --exact         use exact match for function name.
  --cppfilt       use c++filt to demangle.
```

## iouring-dump

Dump the iouring area (x64 only).


### Syntax

```text
usage: iouring-dump [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## link-map

Dump useful members of link_map with iterating.


### Syntax

```text
usage: link-map [-h] [-e ELF_ADDRESS | -l LINK_MAP_ADDRESS] [-n] [-v]

options:
  -h, --help           show this help message and exit
  -e ELF_ADDRESS       the ELF address to parse.
  -l LINK_MAP_ADDRESS  the link_map address to parse.
  -n, --no-pager       do not use the pager.
  -v, --verbose        verbose output.
```

### Examples

```gdb
link-map                    # dump itself
link-map -e 0x555555554000  # dump specified address as ELF
link-map -l 0x7ffff7ffe2e0  # dump specified address as link_map
```

## stdio-dump

Dump members of stdin/stdout/stderr.

- Alias: `fp`

### Syntax

```text
usage: stdio-dump [-h] [-n] [address ...]

positional arguments:
  address         the ELF address to parse (default: stdin, stdout, stderr).

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

# 02-f. Process Information - Security
## aslr

View / modify the ASLR setting of GDB.


### Syntax

```text
usage: aslr [-h] [{on,off}]

positional arguments:
  {on,off}    set gdb aslr settings.

options:
  -h, --help  show this help message and exit
```

## canary

Display the canary value of the current process from auxv information.


### Syntax

```text
usage: canary [-h]

options:
  -h, --help  show this help message and exit
```

## capability

Display the capabilities of the debugging process.


### Syntax

```text
usage: capability [-h] [-n] [-v]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   also display detailed bit information other than cap_eff.
```

## checksec

Check the security properties of the current executable or passed as argument.

- Alias: `cs`

### Syntax

```text
usage: checksec [-h] [-r] [-f FILE]

options:
  -h, --help       show this help message and exit
  -r, --remote     parse remote binary if download feature is available.
  -f, --file FILE  the file path to parse.
```

### Examples

```gdb
checksec -f /bin/ls
checksec -r
```

## exploitable

Heuristically classify the exploitability of the current crash.


### Syntax

```text
usage: exploitable [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --verbose  show every signal/heuristic detail that fed the risk rating.
```

### Examples

```gdb
exploitable
```

### Notes

```text
Inspects the current stop (a fatal signal) and gives an MSEC !exploitable-style
rating: EXPLOITABLE / PROBABLY_EXPLOITABLE / PROBABLY_NOT_EXPLOITABLE / UNKNOWN.
It is a heuristic triage hint (signal, $_siginfo fault address, $pc mapping, and
faulting instruction class), not a proof. Userland x86/x86-64 only.
```

## mte-tags

Display the MTE tag for the specified address (ARM64 only).


### Syntax

```text
usage: mte-tags [-h] ADDRESS [COUNT]

positional arguments:
  ADDRESS     the start address to display the MTE tag.
  COUNT       repeat count for MTE tag displaying (every 16 bytes).

options:
  -h, --help  show this help message and exit
```

## ptr-demangle

Demangle a mangled value by PTR_MANGLE.


### Syntax

```text
usage: ptr-demangle [-h] (--source | VALUE)

positional arguments:
  VALUE       the value to demangle.

options:
  -h, --help  show this help message and exit
  --source    shows the source instead of displaying demangled value.
```

## ptr-mangle

Mangle a pointer value by PTR_MANGLE.


### Syntax

```text
usage: ptr-mangle [-h] (--source | VALUE)

positional arguments:
  VALUE       the value to mangle.

options:
  -h, --help  show this help message and exit
  --source    shows the source instead of displaying mangled value.
```

## search-mangled-ptr

Search for mangled values in RW memory.

- Alias: `cookie`

### Syntax

```text
usage: search-mangled-ptr [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --verbose  shows the section currently being searched.
```

# 02-g. Process Information - Symbol
## magic

Display useful userland addresses and offsets.


### Syntax

```text
usage: magic [-h] [-s] [-j] [FILTER ...]

positional arguments:
  FILTER                filter string.

options:
  -h, --help            show this help message and exit
  -s, --smart           show only the most frequently used items.
  -j, --print-file-jumps
                        print _IO_xxx_jumps functions.
```

## symbols

List all symbols (shortcut for `maintenance print msymbols`) with coloring.


### Syntax

```text
usage: symbols [-h] [-t TYPE] [-c] [-n] [-q]

options:
  -h, --help       show this help message and exit
  -t, --type TYPE  filter by symbol type.
  -c, --use-cache  use previous result.
  -n, --no-pager   do not use the pager.
  -q, --quiet      quiet execution.
```

# 02-h. Process Information - Type
## dt

Make it easier to use `ptype /ox TYPE` and `p ((TYPE*) ADDRESS)[0]`.


### Syntax

```text
usage: dt [-h] [-s] [-n] TYPE [ADDRESS]

positional arguments:
  TYPE            the type name.
  ADDRESS         the address to apply the type.

options:
  -h, --help      show this help message and exit
  -s, --smart     override `context.smart_cpp_function_name = True` temporarily.
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
dt "struct malloc_state"       # shortcut for `ptype /ox struct malloc_state`
dt "struct malloc_state" $rsp  # shortcut for `p ((struct malloc_state*) $rsp)[0]`
```

### Notes

```text
This command is designed for several purposes.
1. When displaying very large struct, you may want to go through a pager because the results will not fit on one screen.
   However, using a pager, the color information disappears. This command calls the pager with preserving colors.
2. When `ptype /ox TYPE`, interpreting member type recursively often result is too long and difficult to read.
   This command keeps result compact by displaying only top-level members.
3. When `p ((TYPE*) ADDRESS)[0]` for large struct, the gdb setting of `max-value-size` is too small to display.
   This command adjusts it automatically.
4. When debugging a binary written in the Golang, the offset information of the type is not displayed.
   This command also displays the offset.
5. When debugging a binary written in the Golang, the `p ((TYPE*) ADDRESS)[0]` command will be broken.
   This is because the Golang helper script is automatically loaded and overwrites the behavior of `p` command.
   This command creates the display results on the python side, so we can display it without any problems.
```

## types

List all types (shortcut for `info types`) with compaction.


### Syntax

```text
usage: types [-h] [-s] [-f FILTER] [-e EXCLUDE] [-E] [-S] [-T] [-U] [-c] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -s, --smart           temporarily override by `context.smart_cpp_function_name = True`.
  -f, --filter FILTER   REGEXP include filter.
  -e, --exclude EXCLUDE
                        REGEXP exclude filter.
  -E, --no-enum         without enum.
  -S, --no-struct       without struct.
  -T, --no-typedef      without typedef.
  -U, --no-union        without union.
  -c, --use-cache       use previous result.
  -n, --no-pager        do not use the pager.
  -v, --verbose         with the output of `dt` command.
```

# 03-a. Memory - Search
## find-syscall

Find the syscall gadget.


### Syntax

```text
usage: find-syscall [-h] [-b NB_INSNS_BEFORE] [-s MAX_REGION_SIZE] [-n] [SECTION_OR_START_ADDR] [SIZE]

positional arguments:
  SECTION_OR_START_ADDR
                        section name or starting address of search range.
  SIZE                  search range size. valid only when a start address is specified.

options:
  -h, --help            show this help message and exit
  -b, --nb-insns-before NB_INSNS_BEFORE
                        the number of previous lines when print syscall instruction.
  -s, --max-region-size MAX_REGION_SIZE
                        maximum search region size. (default: 0x10000000; 0: infinity)
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
find-syscall libc                   # search syscall from libc .text
find-syscall binary                 # 'binary' means the area executable itself (usermode only)
find-syscall 0x400000-0x404000      # search syscall from specific range
find-syscall 0x400000 0x4000        # another valid format
```

## scan-section

Find memory addresses mapped across different regions.

- Alias: `peek-pointers`, `leakfind`, `p2p`

### Syntax

```text
usage: scan-section [-h] [HAYSTACK] [NEEDLE]

positional arguments:
  HAYSTACK    where to search for the needle.
  NEEDLE      what to search for.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
scan-section stack binary                        # scan binary address from stack
scan-section stack libc                          # scan libc address from stack
scan-section stack heap                          # scan heap address from stack
scan-section heap libc                           # scan libc address from heap
scan-section 0x555555772000-0x555555774000 libc  # support address range
scan-section any any
```

## search-cfi-gadgets

Search for CFI-valid, controllable gadgets in the executable area.


### Syntax

```text
usage: search-cfi-gadgets [-h] [-r] [-n]

options:
  -h, --help      show this help message and exit
  -r, --rescan    do not use cache.
  -n, --no-pager  do not use the pager.
```

## search-pattern

Search for a pattern in memory.

- Alias: `xfind`, `xf`

### Syntax

```text
usage: search-pattern [-h] [--hex | --hex-regex] [-d] [-b] [-a ALIGNED] [-p PERM] [-i INTERVAL] [-l LIMIT] [-s MAX_REGION_SIZE] [--phys] [-k | -u] [-v] [-q] [-Q] [-S] PATTERN [SECTION_OR_START_ADDR] [SIZE]

positional arguments:
  PATTERN               search target value. "double-escaped string" or 0xXXXXXXXX style.
  SECTION_OR_START_ADDR
                        section name or starting address of search range.
  SIZE                  search range size. valid only when a start address is specified.

options:
  -h, --help            show this help message and exit
  --hex                 interpret PATTERN as hex. invalid characters are ignored.
  --hex-regex           interpret PATTERN as hex with REGEX-style. space is ignored.
  -d, --disable-utf16   disable utf16 search if PATTERN is ascii string.
  -b, --big             interpret PATTERN as big endian if PATTERN is 0xXXXXXXXX style.
  -a, --aligned ALIGNED
                        alignment unit. (default: 1)
  -p, --perm PERM       the filter by permission. (default: r??)
  -i, --interval INTERVAL
                        the interval to skip searching from the last found position within the same section.
  -l, --limit LIMIT     the limit of the search result.
  -s, --max-region-size MAX_REGION_SIZE
                        maximum search region size. (default: 0x10000000; 0: infinity)
  --phys                treat START_ADDR as a physical address (available in qemu-system).
  -k, --kernel-only     search from kernel area (available in qemu-system).
  -u, --user-only       search from user area (available in qemu-system).
  -v, --verbose         shows the section currently being searched.
  -q, --quiet           suppress warnings.
  -Q, --quiet-region    suppress region information.
  -S, --quiet-symbol    not shown even if symbol exists.
```

### Examples

```gdb
search-pattern ABCD                        # search for 'ABCD' from whole memory
search-pattern "\\x41\\x42\\x43\\x44"      # double-escaped string is also valid
search-pattern --hex "41 42 43 44"         # another valid format
search-pattern --hex-regex "4[0-9]424344"  # hex regex search
search-pattern 0x44434241                  # search for 0x44434241 (='ABCD') from whole memory
search-pattern 0x555555554000 stack        # search for 0x555555554000 (6byte) from stack
search-pattern 0x0000555555554000 stack    # search for 0x0000555555554000 (8byte) from stack
search-pattern AAAA binary                 # 'binary' means the area executable itself (usermode only)
search-pattern AAAA 0x400000-0x404000      # search for 'AAAA' from specific range
search-pattern AAAA 0x400000 0x4000        # another valid format
search-pattern AAAA heap --aligned 16      # search for 'AAAA' with 16-byte alignment
search-pattern AAAA -p r?-                 # search for 'AAAA' from r-- or rw-, but not from r-x or rwx
```

### Notes

```text
To efficiently search large memory regions, the search is usually performed internally by dividing
the region into chunks. The chunk size is 0x10 pages for qemu-system, and 0x400 pages for others.

However, when the --hex-regex option is enabled, this chunked search is disabled,
because it is difficult to implement regular expression searches that span multiple chunks.
```

## strings

Search ASCII string (recursively) from specific location.


### Syntax

```text
usage: strings [-h] [-f FILTER] [-e EXCLUDE] [-d DEPTH] [-r RANGE] [-s] [-m MINLEN] [-n] LOCATION [END_LOCATION]

positional arguments:
  LOCATION              the start location to search for.
  END_LOCATION          the end location to search for. (default: end of region or LOCATION+0x1000)

options:
  -h, --help            show this help message and exit
  -f, --filter FILTER   REGEXP include filter.
  -e, --exclude EXCLUDE
                        REGEXP exclude filter.
  -d, --depth DEPTH     recursive depth. (default: 0)
  -r, --range RANGE     search range for recursively. (default: 64)
  -s, --skip-save       do not save the output.
  -m, --minlen MINLEN   minimum string length (default: 7)
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
strings 0x00007ffffffde000 0x00007ffffffff000             # exact specification
strings 0x00007ffffffde000                                # guess the search end location
strings -m 10 0x00007ffffffde000 0x00007ffffffff000       # filter by length
strings -d 1 0x00007ffffffde000 0x00007ffffffff000        # if an address is found, it will be followed up
strings -f "GLIBC" 0x00007ffffffde000 0x00007ffffffff000  # filter by keywords (-f, -e). need double-escape
```

## xref-telescope

Recursively search for cross-references to a pattern in memory.


### Syntax

```text
usage: xref-telescope [-h] [-v] [-n] PATTERN [DEPTH]

positional arguments:
  PATTERN         search pattern.
  DEPTH           max recursive depth. (default: 1)

options:
  -h, --help      show this help message and exit
  -v, --verbose   shows the section currently being searched.
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
xref-telescope AAAA 2                    # search string with depth level 2
xref-telescope "\\x41\\x41\\x41\\x41" 2  # use double-escape string
xref-telescope 0x555555554000 2          # search value
```

### Notes

```text
To efficiently search large memory regions, the search is usually performed internally by dividing
the region into chunks. The chunk size is 0x10 pages for qemu-system, and 0x400 pages for others.

However, when the --hex-regex option is enabled, this chunked search is disabled,
because it is difficult to implement regular expression searches that span multiple chunks.
```

## xref-to-string

Find xref to specified string (shortcut for `xref-telescope STRING 2`).


### Syntax

```text
usage: xref-to-string [-h] [-n] STRING

positional arguments:
  STRING          search string.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

# 03-b. Memory - View
## hexdump

Display the hexdump from the memory location specified.

- Alias: `hd`

### Syntax

```text
usage: hexdump [-h] [--phys] [-r] [-f] [-s] [-n] [{byte,word,dword,qword}] LOCATION [COUNT]

positional arguments:
  {byte,word,dword,qword}
                        dump mode. It also works if you specify the first character. (default: byte)
  LOCATION              the memory address to dump.
  COUNT                 the count of displayed units. (default: 256)

options:
  -h, --help            show this help message and exit
  --phys                treat LOCATION as a physical address (qemu-system only).
  -r, --reverse         display in reverse order line by line.
  -f, --full            display the same line without omitting.
  -s, --symbol          display the symbol.
  -n, --no-pager        do not use the pager.
```

## hexdump-flexible

Display the hexdump with user-defined format.


### Syntax

```text
usage: hexdump-flexible [-h] [--phys] [-t IDX TAG] [-n] FORMAT LOCATION [COUNT]

positional arguments:
  FORMAT             dump format.
  LOCATION           the memory address to dump.
  COUNT              the count of displayed units. (default: 1)

options:
  -h, --help         show this help message and exit
  --phys             treat LOCATION as a physical address (qemu-system only).
  -t, --tag IDX TAG  display with tags.
  -n, --no-pager     do not use the pager.
```

### Examples

```gdb
hexdump-flexible "2Q2I2H2B" $rsp 4  # "Show qword*2, dword*2, short*2, byte*2" from $rsp and repeat 4 times
hexdump-flexible "4Q-2Q" $rsp 4     # "Show qword*4 and skip qword*2" from $rsp and repeat 4 times
```

## json

The base command to pretty print for JSON.


### Syntax

```text
usage: json [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## json memory

Pretty print JSON from memory values.


### Syntax

```text
usage: json memory [-h] [-n] LOCATION

positional arguments:
  LOCATION        start address for json.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
json memory $rdi
```

## json value

Pretty print JSON from specified value.


### Syntax

```text
usage: json value [-h] [-n] VALUE

positional arguments:
  VALUE           the string of JSON.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
json value '["foo", {"bar": ["baz", null, 1.0, 2]}]'
```

## sigreturn

Display stack values for sigreturn syscall.


### Syntax

```text
usage: sigreturn [-h] [-n] [LOCATION]

positional arguments:
  LOCATION        the address interpreted as the beginning of a sigframe. (default: current_arch.sp)

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## walk-link-list

Walk the link list.

- Alias: `chain`

### Syntax

```text
usage: walk-link-list [-h] [-o NEXT_OFFSET] [-A DUMP_BYTES_AFTER] [-B DUMP_BYTES_BEFORE] [--adjust-output ADJUST_OUTPUT] [-n] ADDRESS

positional arguments:
  ADDRESS               start address to walk.

options:
  -h, --help            show this help message and exit
  -o NEXT_OFFSET        offset of the next(or prev) pointer in the target structure.
  -A DUMP_BYTES_AFTER   dump bytes after link-list location.
  -B DUMP_BYTES_BEFORE  dump bytes before link-list location.
  --adjust-output ADJUST_OUTPUT
                        displays the result of subtracting a specific value to the output.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
walk-link-list 0xffff9c60800597e0       # walk list_head.next
walk-link-list -o 8 0xffff9c60800597e0  # walk list_head.prev
```

## xc

Dump address like x/x command, but with coloring at some intervals.


### Syntax

```text
usage: xc [-h] [-i INTERVAL] [-c COLOR_NUM] [-n] [-q] [FMT] ADDRESS

positional arguments:
  FMT                   dump format.
  ADDRESS               dump address.

options:
  -h, --help            show this help message and exit
  -i, --interval INTERVAL
                        the line of interval for coloring.
  -c, --color-num COLOR_NUM
                        the number of colors used (1-5).
  -n, --no-pager        do not use the pager.
  -q, --quiet           quiet mode.
```

## xs

Dump string like x/s command, but with hex-string style.


### Syntax

```text
usage: xs [-h] [-l MAX_LENGTH] [-H] [-n] [-q] [COUNT] ADDRESS

positional arguments:
  COUNT                 repeat count for displaying.
  ADDRESS               dump target address.

options:
  -h, --help            show this help message and exit
  -l, --max-length MAX_LENGTH
                        maximum number of characters to display. 0 means unlimited.
  -H, --hex             show in hex style.
  -n, --no-pager        do not use the pager.
  -q, --quiet           quiet mode.
```

## xxd

Display the hexdump from the memory location specified (shortcut for `hexdump byte`).


### Syntax

```text
usage: xxd [-h] [--phys] [-r] [-f] [-s] [-n] LOCATION [COUNT]

positional arguments:
  LOCATION        the memory address to dump.
  COUNT           the count of displayed units. (default: 256)

options:
  -h, --help      show this help message and exit
  --phys          treat LOCATION as a physical address (qemu-system only).
  -r, --reverse   display in reverse order line by line.
  -f, --full      display the same line without omitting.
  -s, --symbol    display the symbol.
  -n, --no-pager  do not use the pager.
```

# 03-c. Memory - Compare
## bincompare

Compare an binary file with the memory position looking for badchars.


### Syntax

```text
usage: bincompare [-h] [--file-offset FILE_OFFSET] [-f] [-n] FILENAME ADDRESS [SIZE]

positional arguments:
  FILENAME              specifies the binary file to be compared.
  ADDRESS               specifies the memory address.
  SIZE                  specifies the size.

options:
  -h, --help            show this help message and exit
  --file-offset FILE_OFFSET
                        specifies the file offset.
  -f, --full            display the same line without omitting.
  -n, --no-pager        do not use the pager.
```

## memcmp

Compare the memory contents of two locations.


### Syntax

```text
usage: memcmp [-h] [--phys1] [--phys2] [-f] [-t] [-n] LOCATION1 LOCATION2 SIZE

positional arguments:
  LOCATION1             first address for comparison.
  LOCATION2             second address for comparison.
  SIZE                  the size for comparison.

options:
  -h, --help            show this help message and exit
  --phys1               treat LOCATION1 as a physical address.
  --phys2               treat LOCATION2 as a physical address.
  -f, --full            display the same line without omitting.
  -t, --telescope-like  compare the output like telescope.
  -n, --no-pager        do not use the pager.
```

# 03-d. Memory - Patch
## memcpy

Copy the contents of one memory to another.


### Syntax

```text
usage: memcpy [-h] [--phys1] [--phys2] TO_ADDRESS FROM_ADDRESS SIZE

positional arguments:
  TO_ADDRESS    destination of memcpy.
  FROM_ADDRESS  source of memcpy.
  SIZE          the size for memcpy.

options:
  -h, --help    show this help message and exit
  --phys1       treat TO_ADDRESS as a physical address.
  --phys2       treat FROM_ADDRESS as a physical address.
```

### Notes

```text
memcpy dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | CCCCCCCC ]

memswap dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | AAAAAAAA ]

meminsert dst src 16 8
           <-------size1-------> <--size2->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | AAAAAAAA | BBBBBBBB ]
```

## meminsert

Insert the contents of one memory to another.


### Syntax

```text
usage: meminsert [-h] [--phys1] [--phys2] TO_ADDRESS FROM_ADDRESS SIZE1 SIZE2

positional arguments:
  TO_ADDRESS    destination of meminsert.
  FROM_ADDRESS  source of meminsert.
  SIZE1         the pushed back size for meminsert.
  SIZE2         the inserted(slided) size for meminsert.

options:
  -h, --help    show this help message and exit
  --phys1       treat TO_ADDRESS as a physical address.
  --phys2       treat FROM_ADDRESS as a physical address.
```

### Notes

```text
memcpy dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | CCCCCCCC ]

memswap dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | AAAAAAAA ]

meminsert dst src 16 8
           <-------size1-------> <--size2->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | AAAAAAAA | BBBBBBBB ]
```

## memset

Set the value to the memory range.


### Syntax

```text
usage: memset [-h] [--phys] TO_ADDRESS VALUE SIZE

positional arguments:
  TO_ADDRESS  destination of memset.
  VALUE       the value to write.
  SIZE        the size for memset.

options:
  -h, --help  show this help message and exit
  --phys      treat TO_ADDRESS as a physical address.
```

### Examples

```gdb
memset $rsp 0xff 0x20
```

### Notes

```text
If you want to specify a large value for `VALUE`, use the `patch string` command.
```

## memswap

Swap the contents of one memory to another.


### Syntax

```text
usage: memswap [-h] [--phys1] [--phys2] SWAP_ADDRESS1 SWAP_ADDRESS2 SIZE

positional arguments:
  SWAP_ADDRESS1  swap target address.
  SWAP_ADDRESS2  another swap target address.
  SIZE           the size for memory swap.

options:
  -h, --help     show this help message and exit
  --phys1        treat SWAP_ADDRESS1 as a physical address.
  --phys2        treat SWAP_ADDRESS2 as a physical address.
```

### Notes

```text
memcpy dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | CCCCCCCC ]

memswap dst src 8
                                 <--size-->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | BBBBBBBB | AAAAAAAA ]

meminsert dst src 16 8
           <-------size1-------> <--size2->
            dst                   src
  Before: [ AAAAAAAA | BBBBBBBB | CCCCCCCC ]
  After : [ CCCCCCCC | AAAAAAAA | BBBBBBBB ]
```

## patch

The base command to write specified values to the specified address.


### Syntax

```text
usage: patch [-h] {byte,word,dword,qword,string,hex,pattern,nop,inf,trap,ret,syscall,range-replace,history,revert} ...

options:
  -h, --help            show this help message and exit

command:
  {byte,word,dword,qword,string,hex,pattern,nop,inf,trap,ret,syscall,range-replace,history,revert}
```

## patch byte

Write specified BYTE to the specified address.

- Alias: `patch b`

### Syntax

```text
usage: patch byte [-h] [-e] [--phys] LOCATION BYTE [BYTE ...]

positional arguments:
  LOCATION    the memory address to patch.
  BYTE        the value to patch.

options:
  -h, --help  show this help message and exit
  -e          reverse endian.
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch byte    $rip 0x41 0x41 0x41 0x41 0x41
patch byte -e $rip 0x41 0x41 0x41 0x41 0x41  # -e is ignored
```

## patch dword

Write specified DWORD to the specified address.

- Alias: `patch d`

### Syntax

```text
usage: patch dword [-h] [-e] [--phys] LOCATION DWORD [DWORD ...]

positional arguments:
  LOCATION    the memory address to patch.
  DWORD       the value to patch.

options:
  -h, --help  show this help message and exit
  -e          reverse endian.
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch dword    $rip 0x41424344  # write `DCBA` to [rip]
patch dword -e $rip 0x41424344  # write `ABCD` to [rip]
```

## patch hex

Write specified hex string to the specified address.


### Syntax

```text
usage: patch hex [-h] [--phys] LOCATION "hex-string" [LENGTH]

positional arguments:
  LOCATION      the memory address to patch.
  "hex-string"  the string to write to memory.
  LENGTH        the number of bytes to patch. (default: None)

options:
  -h, --help    show this help message and exit
  --phys        treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch hex $sp "4141414142424242"
```

## patch history

Display the patch history stack.

- Alias: `patch list`

### Syntax

```text
usage: patch history [-h] [-n] [-v]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   verbose output.
```

## patch inf

Patch the instruction(s) at the given address with an infinite loop.


### Syntax

```text
usage: patch inf [-h] [--phys] [LOCATION]

positional arguments:
  LOCATION    the memory address to patch. (default: current_arch.pc)

options:
  -h, --help  show this help message and exit
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch inf $pc
```

## patch nop

Patch the instruction(s) at the given address with NOP.

- Alias: `nop`

### Syntax

```text
usage: patch nop [-h] [--phys] [-b BYTE_LENGTH | -i INST_COUNT] [LOCATION]

positional arguments:
  LOCATION        the memory address to patch. (default: current_arch.pc)

options:
  -h, --help      show this help message and exit
  --phys          treat LOCATION as a physical address (qemu-system only).
  -b BYTE_LENGTH  the patch length in bytes. (default: None)
  -i INST_COUNT   the number of instructions to patch. (default: 1)
```

### Examples

```gdb
patch nop $pc -i 2
```

## patch pattern

Write a pattern string to the specified memory address.


### Syntax

```text
usage: patch pattern [-h] [--phys] [-c CHARSET] [-d] LOCATION LENGTH

positional arguments:
  LOCATION              the memory address to patch.
  LENGTH                the number of bytes to patch. (default: None)

options:
  -h, --help            show this help message and exit
  --phys                treat LOCATION as a physical address (qemu-system only).
  -c, --charset CHARSET
                        the charset of the pattern. (default: abc..z)
  -d, --dry-run         only generate patterns (do not patch memory).
```

### Examples

```gdb
patch pattern $sp 128
```

## patch qword

Write specified QWORD to the specified address.

- Alias: `patch q`

### Syntax

```text
usage: patch qword [-h] [-e] [--phys] LOCATION QWORD [QWORD ...]

positional arguments:
  LOCATION    the memory address to patch.
  QWORD       the value to patch.

options:
  -h, --help  show this help message and exit
  -e          reverse endian.
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch qword    $rip 0x4142434445464748  # write `HGFEDCBA` to [rip]
patch qword -e $rip 0x4142434445464748  # write `ABCDEFGH` to [rip]
```

## patch range-replace

Replace all occurrences of a specific byte sequence in the specified range with another byte sequence.


### Syntax

```text
usage: patch range-replace [-h] [--phys] START_ADDR END_ADDR HEX_STR_FROM HEX_STR_TO

positional arguments:
  START_ADDR    start address to search.
  END_ADDR      end address to search.
  HEX_STR_FROM  the hex string to search for (source pattern).
  HEX_STR_TO    the hex string to replace it with (replacement pattern).

options:
  -h, --help    show this help message and exit
  --phys        treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch range-replace 0x400000 0x401000 "ebfe" "9090"
```

## patch ret

Patch the instruction(s) at the given address with return.


### Syntax

```text
usage: patch ret [-h] [--phys] [LOCATION]

positional arguments:
  LOCATION    the memory address to patch. (default: current_arch.pc)

options:
  -h, --help  show this help message and exit
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch ret $pc
```

## patch revert

Revert patches recorded in the patch history stack.


### Syntax

```text
usage: patch revert [-h] (--all | TARGET_STATE)

positional arguments:
  TARGET_STATE  the history state index number to revert.

options:
  -h, --help    show this help message and exit
  --all         revert all patches.
```

### Examples

```gdb
patch revert 0  # do nothing (keep the current state).
patch revert 2  # roll back to history state [2].
```

## patch string

Write specified string to the specified memory address.


### Syntax

```text
usage: patch string [-h] [--phys] LOCATION "double backslash-escaped string" [LENGTH]

positional arguments:
  LOCATION              the memory address to patch.
  "double backslash-escaped string"
                        the string to write to memory.
  LENGTH                the number of bytes to patch. (default: None)

options:
  -h, --help            show this help message and exit
  --phys                treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch string $sp "AAAABBBB"
patch string $sp "\\x41\\x41\\x41\\x41\\x42\\x42\\x42\\x42"
```

## patch syscall

Patch the instruction(s) at the given address with syscall instruction.


### Syntax

```text
usage: patch syscall [-h] [--phys] [LOCATION]

positional arguments:
  LOCATION    the memory address to patch. (default: current_arch.pc)

options:
  -h, --help  show this help message and exit
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch syscall $pc
```

## patch trap

Patch the instruction(s) at the given address with breakpoint or trap (if available).


### Syntax

```text
usage: patch trap [-h] [--phys] [LOCATION]

positional arguments:
  LOCATION    the memory address to patch. (default: current_arch.pc)

options:
  -h, --help  show this help message and exit
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch trap $pc
```

## patch word

Write specified WORD to the specified address.

- Alias: `patch w`

### Syntax

```text
usage: patch word [-h] [-e] [--phys] LOCATION WORD [WORD ...]

positional arguments:
  LOCATION    the memory address to patch.
  WORD        the value to patch.

options:
  -h, --help  show this help message and exit
  -e          reverse endian.
  --phys      treat LOCATION as a physical address (qemu-system only).
```

### Examples

```gdb
patch word    $rip 0x4142  # write `BA` to [rip]
patch word -e $rip 0x4142  # write `AB` to [rip]
```

## stub

Stub out the specified function to skip it. (e.g., fork)

- Alias: `deactivate`

### Syntax

```text
usage: stub [-h] [-r RETVAL] LOCATION

positional arguments:
  LOCATION             address/symbol to stub out.

options:
  -h, --help           show this help message and exit
  -r, --retval RETVAL  the return value from stub. (default: 0)
```

### Examples

```gdb
stub -r 0 fork
```

# 03-e. Memory - Calculation
## base-n-decode

The base command to decode baseN.


### Syntax

```text
usage: base-n-decode [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## base-n-decode memory

Decode baseN from memory values.


### Syntax

```text
usage: base-n-decode memory [-h] [-n] LOCATION SIZE

positional arguments:
  LOCATION        start address for baseN decoding.
  SIZE            the size for baseN decoding.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
base-n-decode memory $rsp 0x20
```

## base-n-decode value

Decode baseN from specified values.


### Syntax

```text
usage: base-n-decode value [-h] [--hex] [-n] VALUE

positional arguments:
  VALUE           the string for baseN decoding.

options:
  -h, --help      show this help message and exit
  --hex           interpret VALUE as hex. invalid character is ignored.
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
base-n-decode value "\\x51\\x55\\x46\\x42"
base-n-decode value --hex "51 55 46 42"
```

## base-n-encode

The base command to encode baseN.


### Syntax

```text
usage: base-n-encode [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## base-n-encode memory

Encode baseN from memory values.


### Syntax

```text
usage: base-n-encode memory [-h] [-n] LOCATION SIZE

positional arguments:
  LOCATION        start address for baseN encoding.
  SIZE            the size for baseN encoding.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
base-n-encode memory $rsp 0x20
```

## base-n-encode value

Encode baseN from specified values.


### Syntax

```text
usage: base-n-encode value [-h] [--hex] [-n] VALUE

positional arguments:
  VALUE           the string for baseN encoding.

options:
  -h, --help      show this help message and exit
  --hex           interpret VALUE as hex. invalid character is ignored.
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
base-n-encode value "\\x41\\x42\\x43\\x44"
base-n-encode value --hex "41 42 43 44"
```

## crc

The base command to calculate crc.


### Syntax

```text
usage: crc [-h] {memory,file,value} ...

options:
  -h, --help           show this help message and exit

command:
  {memory,file,value}
```

### Notes

```text
[32b/04B] means 32 bits (4 bytes).
```

## crc file

Calculate crc from file.


### Syntax

```text
usage: crc file [-h] [-f REGEX] [-n] FILE [START_POS] [SIZE]

positional arguments:
  FILE                the filepath for crc calculation.
  START_POS           the start position for crc calculation.
  SIZE                the size for crc calculation.

options:
  -h, --help          show this help message and exit
  -f, --filter REGEX  filter by REGEX pattern.
  -n, --no-pager      do not use the pager.
```

### Notes

```text
[32b/04B] means 32 bits (4 bytes).
```

## crc memory

Calculate crc from memory values.


### Syntax

```text
usage: crc memory [-h] [-f REGEX] [-n] LOCATION SIZE

positional arguments:
  LOCATION            start address for crc calculation.
  SIZE                the size for crc calculation.

options:
  -h, --help          show this help message and exit
  -f, --filter REGEX  filter by REGEX pattern.
  -n, --no-pager      do not use the pager.
```

### Examples

```gdb
crc memory $rsp 0x20
```

### Notes

```text
[32b/04B] means 32 bits (4 bytes).
```

## crc value

Calculate hash from specified values.


### Syntax

```text
usage: crc value [-h] [--hex] [-f REGEX] [-n] VALUE

positional arguments:
  VALUE               the string for crc calculation.

options:
  -h, --help          show this help message and exit
  --hex               interpret VALUE as hex. invalid character is ignored.
  -f, --filter REGEX  filter by REGEX pattern.
  -n, --no-pager      do not use the pager.
```

### Examples

```gdb
crc value "\\x41\\x42\\x43\\x44"
crc value --hex "41 42 43 44"
```

### Notes

```text
[32b/04B] means 32 bits (4 bytes).
```

## hash

The base command to calculate hash.


### Syntax

```text
usage: hash [-h] {memory,file,value,list,test,known-collision} ...

options:
  -h, --help            show this help message and exit

command:
  {memory,file,value,list,test,known-collision}
```

### Notes

```text
[128b/16B] means 128 bits (16 bytes).
The salt for BLAKE2s and BLAKE2b is blank.
The key for KMAC128 and KMAC256 is blank.
The key for SipHash is "\0" * 16.
The key for HalfSipHash is "\0" * 8.
To calculate FSB hash, you need the `gmpy2` package (uv pip install gmpy2).
```

## hash file

Calculate hash from file.


### Syntax

```text
usage: hash file [-h] [-f REGEX] [-l LENGTH_FILTER] [-s] [-n] [-q] FILE [START_POS] [SIZE]

positional arguments:
  FILE                  the filepath for hash calculation.
  START_POS             the start position for hash calculation.
  SIZE                  the size for hash calculation.

options:
  -h, --help            show this help message and exit
  -f, --filter REGEX    filter by REGEX pattern.
  -l, --length-filter LENGTH_FILTER
                        filter by hash byte length.
  -s, --smart           increase output smart level. (-s, -ss)
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Notes

```text
[128b/16B] means 128 bits (16 bytes).
The salt for BLAKE2s and BLAKE2b is blank.
The key for KMAC128 and KMAC256 is blank.
The key for SipHash is "\0" * 16.
The key for HalfSipHash is "\0" * 8.
To calculate FSB hash, you need the `gmpy2` package (uv pip install gmpy2).
```

## hash known-collision

Show hash collision example.


### Syntax

```text
usage: hash known-collision [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Notes

```text
[128b/16B] means 128 bits (16 bytes).
The salt for BLAKE2s and BLAKE2b is blank.
The key for KMAC128 and KMAC256 is blank.
The key for SipHash is "\0" * 16.
The key for HalfSipHash is "\0" * 8.
To calculate FSB hash, you need the `gmpy2` package (uv pip install gmpy2).
```

## hash list

List hash supported by GEF.


### Syntax

```text
usage: hash list [-h] [-f REGEX] [-l LENGTH_FILTER] [-s] [-n]

options:
  -h, --help            show this help message and exit
  -f, --filter REGEX    filter by REGEX pattern.
  -l, --length-filter LENGTH_FILTER
                        filter by hash byte length.
  -s, --smart           increase output smart level. (-s, -ss)
  -n, --no-pager        do not use the pager.
```

## hash memory

Calculate hash from memory values.


### Syntax

```text
usage: hash memory [-h] [-f REGEX] [-l LENGTH_FILTER] [-s] [-n] [-q] LOCATION SIZE

positional arguments:
  LOCATION              start address for hash calculation.
  SIZE                  the size for hash calculation.

options:
  -h, --help            show this help message and exit
  -f, --filter REGEX    filter by REGEX pattern.
  -l, --length-filter LENGTH_FILTER
                        filter by hash byte length.
  -s, --smart           increase output smart level. (-s, -ss)
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
hash memory $rsp 0x20
```

### Notes

```text
[128b/16B] means 128 bits (16 bytes).
The salt for BLAKE2s and BLAKE2b is blank.
The key for KMAC128 and KMAC256 is blank.
The key for SipHash is "\0" * 16.
The key for HalfSipHash is "\0" * 8.
To calculate FSB hash, you need the `gmpy2` package (uv pip install gmpy2).
```

## hash test

Calculate and check hash from constant inputs.


### Syntax

```text
usage: hash test [-h] [-f REGEX] [-l LENGTH_FILTER] [-s] [-t | -T] [--size SIZE] [-n]

options:
  -h, --help            show this help message and exit
  -f, --filter REGEX    filter by REGEX pattern.
  -l, --length-filter LENGTH_FILTER
                        filter by hash byte length.
  -s, --smart           show only failed.
  -t, --time            measure the time taken to compute the hash using large bytes of data.
  -T, --time-with-sort  measure and sort the time taken to compute the hash using large bytes of data.
  --size SIZE           the data size of 'AAAA...' to measure the time taken to compute the hash.
  -n, --no-pager        do not use the pager.
```

## hash value

Calculate hash from specified values.


### Syntax

```text
usage: hash value [-h] [--hex] [-f REGEX] [-l LENGTH_FILTER] [-s] [-n] [-q] VALUE

positional arguments:
  VALUE                 the string for hash calculation.

options:
  -h, --help            show this help message and exit
  --hex                 interpret VALUE as hex. invalid character is ignored.
  -f, --filter REGEX    filter by REGEX pattern.
  -l, --length-filter LENGTH_FILTER
                        filter by hash byte length.
  -s, --smart           increase output smart level. (-s, -ss)
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
hash value "\\x41\\x42\\x43\\x44"
hash value --hex "41 42 43 44"
```

### Notes

```text
[128b/16B] means 128 bits (16 bytes).
The salt for BLAKE2s and BLAKE2b is blank.
The key for KMAC128 and KMAC256 is blank.
The key for SipHash is "\0" * 16.
The key for HalfSipHash is "\0" * 8.
To calculate FSB hash, you need the `gmpy2` package (uv pip install gmpy2).
```

## is-mem-zero

Check if all the memory in the specified range is 0x00, 0xff.


### Syntax

```text
usage: is-mem-zero [-h] [--phys] ADDRESS SIZE

positional arguments:
  ADDRESS     target address for checking.
  SIZE        the size for checking.

options:
  -h, --help  show this help message and exit
  --phys      treat ADDRESS as a physical address.
```

## morse-decode

The base command to decode morse code.


### Syntax

```text
usage: morse-decode [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## morse-decode memory

Decode morse code from memory values.


### Syntax

```text
usage: morse-decode memory [-h] LOCATION SIZE

positional arguments:
  LOCATION    start address for morse code decoding.
  SIZE        the size for morse code decoding.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
morse-decode memory $rsp 0x20
```

## morse-decode value

Decode morse code from specified values.


### Syntax

```text
usage: morse-decode value [-h] VALUE

positional arguments:
  VALUE       the string for morse code decoding.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
morse-decode value -- ".- -... -.-. -.."
```

## morse-encode

The base command to encode morse code.


### Syntax

```text
usage: morse-encode [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## morse-encode memory

Encode morse code from memory values.


### Syntax

```text
usage: morse-encode memory [-h] LOCATION SIZE

positional arguments:
  LOCATION    start address for morse code encoding.
  SIZE        the size for morse code encoding.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
morse-encode memory $rsp 0x20
```

## morse-encode value

Encode morse code from specified values.


### Syntax

```text
usage: morse-encode value [-h] VALUE

positional arguments:
  VALUE       the string for morse code encoding.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
morse-encode value AAAA
```

## seq-length

Detect consecutive length of the same sequence.


### Syntax

```text
usage: seq-length [-h] [--phys] ADDRESS [UNIT]

positional arguments:
  ADDRESS     target address for checking.
  UNIT        the size for a target value (default: 1).

options:
  -h, --help  show this help message and exit
  --phys      treat ADDRESS as a physical address.
```

## strlen

Detect the length of the string.


### Syntax

```text
usage: strlen [-h] [--phys] ADDRESS

positional arguments:
  ADDRESS     target address for checking.

options:
  -h, --help  show this help message and exit
  --phys      treat ADDRESS as a physical address.
```

## xor-memory

The base command to xor a block of memory.


### Syntax

```text
usage: xor-memory [-h] {display,patch} ...

options:
  -h, --help       show this help message and exit

command:
  {display,patch}
```

## xor-memory display

Display a block of memory by xor-ing each byte with specified key.


### Syntax

```text
usage: xor-memory display [-h] [-n] LOCATION SIZE KEY

positional arguments:
  LOCATION        the address of data to xor.
  SIZE            the size of data to xor.
  KEY             the data to xor as key.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
xor-memory display $sp 16 41414141
```

## xor-memory patch

Patch a block of memory by xor-ing each byte with specified key.


### Syntax

```text
usage: xor-memory patch [-h] LOCATION SIZE KEY

positional arguments:
  LOCATION    the address of data to xor.
  SIZE        the size of data to xor.
  KEY         the data to xor as key.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
xor-memory patch $sp 16 41414141
```

# 03-f. Memory - Dump/Load
## load-file

Load the file into memory.


### Syntax

```text
usage: load-file [-h] LOCATION FILE_PATH [FILE_OFFSET] [LOAD_SIZE]

positional arguments:
  LOCATION     the memory address to load.
  FILE_PATH    the filepath to load.
  FILE_OFFSET  the offset of the file to load.
  LOAD_SIZE    the size of the data to load.

options:
  -h, --help   show this help message and exit
```

### Notes

```text
+-memory------+
|             |             +-file_start--+
|             |             | ^           |
|             |             | |           |
|             |             | v           |
| LOCATION <----------------- FILE_OFFSET |
| ...         | ^           | ...         |
|             | | LOAD_SIZE |             |
| ...         | v           | ...         |
| end <---------------------- end         |
|             |             |             |
|             |             |             |
|             |             +-file_end----+
|             |
+-------------+
If there is not enough space, the load will fail halfway.
```

## load-file-mmap

Load the file into memory that allocated by `mmap`.


### Syntax

```text
usage: load-file-mmap [-h] LOCATION FILE_PATH [FILE_OFFSET] [LOAD_SIZE]

positional arguments:
  LOCATION     the memory address to load.
  FILE_PATH    the filepath to load.
  FILE_OFFSET  the offset of the file to load.
  LOAD_SIZE    the size of the data to load.

options:
  -h, --help   show this help message and exit
```

### Notes

```text
+-mmap_start--+
|             |             +-file_start--+
|             |             | ^           |
|             |             | |           |
|             |             | v           |
| LOCATION <----------------- FILE_OFFSET |
| ...         | ^           | ...         |
|             | | LOAD_SIZE |             |
| ...         | v           | ...         |
| end <---------------------- end         |
|             |             |             |
|             |             |             |
|             |             +-file_end----+
|             |
+-mmap_end----+
```

## smart-memory-dump

Dump the memory of the entire process smartly.


### Syntax

```text
usage: smart-memory-dump [-h] [-p PREFIX] [-s SUFFIX] [-f FILTER] [-e EXCLUDE] [-c] [-m MAX_REGION_SIZE]

options:
  -h, --help            show this help message and exit
  -p, --prefix PREFIX   use this name for the dump destination file prefix. (default: '')
  -s, --suffix SUFFIX   use this name for the dump destination file suffix. (default: '')
  -f, --filter FILTER   REGEXP include filter.
  -e, --exclude EXCLUDE
                        REGEXP exclude filter.
  -c, --commit          actually perform the dump.
  -m, --max-region-size MAX_REGION_SIZE
                        maximum size of dump region. (default: 0x10000000; 0: infinity)
```

# 03-g. Memory - Investigation
## binwalk-memory

Scan memory by binwalk.


### Syntax

```text
usage: binwalk-memory [-h] [-f FILTER] [-e EXCLUDE] [-m MAXSIZE] [-c]

options:
  -h, --help            show this help message and exit
  -f, --filter FILTER   REGEXP include filter.
  -e, --exclude EXCLUDE
                        REGEXP exclude filter.
  -m, --maxsize MAXSIZE
                        maximum size of a section to be dumped. (default: 256 MB)
  -c, --commit          actually perform binwalk.
```

## filetype-memory

Scan memory by file and magika.


### Syntax

```text
usage: filetype-memory [-h] ADDRESS [END_ADDRESS]

positional arguments:
  ADDRESS      target address.
  END_ADDRESS  target end address. (default: the end of section of ADDRESS)

options:
  -h, --help   show this help message and exit
```

## freq-analysis

Visualize the frequency of occurrence of each byte.


### Syntax

```text
usage: freq-analysis [-h] [-e EXCLUDE] [-a] [-t TOPN] [-n] LOCATION [SIZE]

positional arguments:
  LOCATION              start address to analyze.
  SIZE                  the size to analyze; if omitted, calculated from the end of the area.

options:
  -h, --help            show this help message and exit
  -e, --exclude EXCLUDE
                        exclude character in hex.
  -a, --ascii-gradation
                        show heatmap with ascii range word.
  -t, --topn TOPN       outputs the top N numbers. (default: 16)
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
freq-analysis $rax 0x1000               # ragne: $rax ~ $rax + 0x1000
freq-analysis $rax                      # range: $rax ~ end of the region to which $rax belongs
freq-analysis $rax 0x1000 -a            # use ascii compatible result
freq-analysis $rax 0x1000 -e 00 -e 01   # exclude some characters
```

## peek-pageflags

Read the page flags of a page frame (needs root).

- Alias: `ppfl`

### Syntax

```text
usage: peek-pageflags [-h] [-n] PFN

positional arguments:
  PFN             pfn of which to read flags.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
peek-pageflags 0x6b2ae3
```

## peek-pageframe

Read page frame data from a single address or an address range.

- Alias: `ppf`

### Syntax

```text
usage: peek-pageframe [-h] [-f FROM_ADDR] [-t TO_ADDR] [-i] [-n] [ADDRESS]

positional arguments:
  ADDRESS               address for which the pfn is read.

options:
  -h, --help            show this help message and exit
  -f, --from-addr FROM_ADDR
                        start of range.
  -t, --to-addr TO_ADDR
                        end of range.
  -i, --ignore-non-present
                        ignores pages which are not present in the output.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
peek-pageframe 0x555555555060                       # read pagemap of single address
peek-pageframe -f 0x7ffffffdd000 -t 0x7ffffffff000  # read pagemap of an address range
```

## sixel-memory

Show image (png, jpg, bmp, etc.) to terminal by imagemagick.


### Syntax

```text
usage: sixel-memory [-h] [-b] LOCATION [SIZE]

positional arguments:
  LOCATION              start address of the image.
  SIZE                  the size of the image.

options:
  -h, --help            show this help message and exit
  -b, --decode-barcode  decode barcode if found.
```

## vdump

Visualize memory data like an image.


### Syntax

```text
usage: vdump [-h] [-d] [-w WIDTH] [-c {r,g,b}] [-n] [-A] [-Ab AUTO_INCLEMENT_BEGIN_WIDTH] [-Ae AUTO_INCLEMENT_END_WIDTH] [-As AUTO_INCLEMENT_STEP_WIDTH] LOCATION [SIZE]

positional arguments:
  LOCATION              start address to dump.
  SIZE                  the size to dump; if omitted, calculated from the end of the area.

options:
  -h, --help            show this help message and exit
  -d, --disable-autoscale
                        disable autoscaling to fit the terminal.
  -w, --width WIDTH     the number of wrap bytes. (default: sqrt(len(content)))
  -c, --color {r,g,b}   convert the grayscale tone to either r,g,b.
  -n, --negate          negate the grayscale tone.
  -A, --auto-width-inclement
                        repeat the display while shifting the interpretation of the width.
  -Ab, --auto-inclement-begin-width AUTO_INCLEMENT_BEGIN_WIDTH
                        auto inclement begin width. (default: 16)
  -Ae, --auto-inclement-end-width AUTO_INCLEMENT_END_WIDTH
                        auto inclement end width. (default: min(len(data) // begin_width, 512)
  -As, --auto-inclement-step-width AUTO_INCLEMENT_STEP_WIDTH
                        auto inclement step width. (default: 2)
```

### Examples

```gdb
vdump $rsp 0x1000                                 # width =~ sqrt(len(content))
vdump -w 0x100 $rsp 0x1000                        # use fixed width
vdump -c r $rsp 0x1000                            # change color: gray -> red
vdump -c r -n $rsp 0x1000                         # change color: gray -> red and negate
vdump -A $rsp 0x1000                              # bruteforce the width
vdump -A -Ab 0x100 -Ae 0x200 -As 0x10 $rsp 0x1000 # bruteforce the width (w=0x100; w<0x200; w+=0x10)
```

# 04-a. Register - View
## avx

Display AVX registers.

- Alias: `ymm`

### Syntax

```text
usage: avx [-h]

options:
  -h, --help  show this help message and exit
```

## avx512

Display AVX512 registers.

- Alias: `zmm`

### Syntax

```text
usage: avx512 [-h]

options:
  -h, --help  show this help message and exit
```

## cpuid

Get cpuid result.


### Syntax

```text
usage: cpuid [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
cpuid
```

### Notes

```text
Disable `-enable-kvm` option for qemu-system.
```

## fpu

Display fpu registers (x86/x64:x87-fpu, ARM/ARM64:vfp-d16).


### Syntax

```text
usage: fpu [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --verbose  also display bit information of fpu control registers.
```

## mmx

Display MMX registers.


### Syntax

```text
usage: mmx [-h]

options:
  -h, --help  show this help message and exit
```

## pac-keys

Pretty-print PAC keys from qemu registers (ARM64 only).


### Syntax

```text
usage: pac-keys [-h]

options:
  -h, --help  show this help message and exit
```

## sse

Display SSE registers.

- Alias: `xmm`

### Syntax

```text
usage: sse [-h] [-v]

options:
  -h, --help     show this help message and exit
  -v, --verbose  also display bit information of mxcsr registers.
```

## sysreg

Pretty-print system registers (not general purpose) from `info register`.


### Syntax

```text
usage: sysreg [-h] [--exact] [FILTER ...]

positional arguments:
  FILTER      filter string.

options:
  -h, --help  show this help message and exit
  --exact     use exact match.
```

# 04-b. Register - Modify
## edit-flags

Edit flags in a human friendly way.


### Syntax

```text
usage: edit-flags [-h] [-v] [[FLAGNAME(+|-|~) ...] ...]

positional arguments:
  [FLAGNAME(+|-|~) ...]
                        the flag name to edit.

options:
  -h, --help            show this help message and exit
  -v, --verbose         show the bit information of the flag register.
```

### Examples

```gdb
edit-flags             # show the flag register
edit-flags zero+       # set ZERO flag
edit-flags direction-  # unset DIRECTION flag
edit-flags sign~       # toggle SIGN flag
edit-flags -v          # verbose output
```

## mmxset

Simply set the value to mm register.


### Syntax

```text
usage: mmxset [-h] REG=VALUE

positional arguments:
  REG=VALUE   MMX register and value to set.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
mmxset $mm0=0x1122334455667788
```

### Notes

```text
Disable `-enable-kvm` option for qemu-system.
```

## xmmset

Simply set the value to xmm or ymm register.


### Syntax

```text
usage: xmmset [-h] REG=VALUE

positional arguments:
  REG=VALUE   XMM/YMM/ZMM register and value to set.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
xmmset $ymm0=0x11223344556677889900aabbccddeeff9876543210
```

# 05-a. Heap - Glibc
## heap

The base command to get information about the Glibc heap structure.


### Syntax

```text
usage: heap [-h] {arena,arenas,bins,bins-simple,chunk,chunks,top,try-free,try-malloc,try-realloc,try-calloc,tcache-index-helper,find-fake-fast,extract-heap-addr,calc-protected-fd,visual-heap,dump-image,tracer,parse,snapshot,snapshot-compare} ...

options:
  -h, --help            show this help message and exit

command:
  {arena,arenas,bins,bins-simple,chunk,chunks,top,try-free,try-malloc,try-realloc,try-calloc,tcache-index-helper,find-fake-fast,extract-heap-addr,calc-protected-fd,visual-heap,dump-image,tracer,parse,snapshot,snapshot-compare}
```

### Notes

```text
Supports up to glibc 2.43.
- 2.15+: GEF treats malloc_par.pagesize as absent (always None).
- 2.19+: malloc_state.next_free is handled.
- 2.23+: malloc_state.attached_threads is handled.
- 2.24+: GEF treats malloc_par.max_total_mem as absent (always None).
- 2.26: tcache is introduced.
- 2.26+: MALLOC_ALIGNMENT changes for x86_32/riscv32/ppc32 affect NFASTBINS and bin-size tables.
- 2.27+: malloc_state layout handling changes (have_fastchunks/fastbins offsets).
- 2.30: tcache_perthread_struct.counts element size changes 1->2 bytes.
- 2.32: Safe-Linking (pointer mangling) for tcache/fastbins fd is supported.
- 2.34+: GEF no longer uses the __malloc_hook-based strategy to locate main_arena.
- 2.35: heap_info.pagesize is handled.
- 2.35: malloc_par.{thp_pagesize,hp_pagesize,hp_flags} are handled.
- 2.42: TCACHE_MAX_BINS 64->76 (+12 large bins, arch-dependent size ranges).
- 2.42: tcache_perthread_struct.counts changes to num_slots.
- 2.43: fastbins are removed.
- 2.43: TCACHE_FILL_COUNT 7->16.
```

## heap arena

Display information on a heap arena.

- Alias: `arena`

### Syntax

```text
usage: heap arena [-h] [-a ARENA_ADDR] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -n, --no-pager        do not use the pager.
```

## heap arenas

List heap arenas.

- Alias: `arenas`

### Syntax

```text
usage: heap arenas [-h]

options:
  -h, --help  show this help message and exit
```

## heap bins

Display information about the bins of an arena.

- Alias: `bins`

### Syntax

```text
usage: heap bins [-h] [-a ARENA_ADDR] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
heap bins
heap bins -a 0x7ffff0000020 -v
heap bins -a 1 -v
```

## heap bins fast

Display information about the fastbinsY of an arena.

- Alias: `fastbins`

### Syntax

```text
usage: heap bins fast [-h] [-a ARENA_ADDR] [-i INDEX_FILTER] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -i, --index-filter INDEX_FILTER
                        filter by fastbins index.
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

## heap bins large

Display information about the Large Bins of an arena.

- Alias: `largebins`

### Syntax

```text
usage: heap bins large [-h] [-a ARENA_ADDR] [-i INDEX_FILTER] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -i, --index-filter INDEX_FILTER
                        filter by largebins index.
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

## heap bins small

Display information about the Small Bins of an arena.

- Alias: `smallbins`

### Syntax

```text
usage: heap bins small [-h] [-a ARENA_ADDR] [-i INDEX_FILTER] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -i, --index-filter INDEX_FILTER
                        filter by smallbins index.
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

## heap bins tcache

Display information about the Tcache of an arena.

- Alias: `tcachebins`

### Syntax

```text
usage: heap bins tcache [-h] [-a ARENA_ADDR] [-i INDEX_FILTER] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -i, --index-filter INDEX_FILTER
                        filter by tcache index.
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

## heap bins unsorted

Display information about the Unsorted Bins of an arena.

- Alias: `unsortedbin`

### Syntax

```text
usage: heap bins unsorted [-h] [-a ARENA_ADDR] [-v] [--all] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
  -n, --no-pager        do not use the pager.
```

## heap bins-simple

Simply display information on the bins of an arena.

- Alias: `bs`, `heapinfo`

### Syntax

```text
usage: heap bins-simple [-h] [-a ARENA_ADDR] [-s] [-v] [--all]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -s, --skip-size       skip size information.
  -v, --verbose         display empty bins.
  --all                 dump all arenas.
```

### Examples

```gdb
heap bins-simple
heap bins-simple -a 0x7ffff0000020 -v
heap bins-simple -a 1 -v
```

### Notes

```text
The meaning of the tcache expression:
  e.g.; 0x80 [6] (1): 0x55555557e480
    0x80: size; [6]: tcache index; (1): tcache_perthread_struct.count[i]
```

## heap calc-protected-fd

Calculate a valid value as protected `fd` pointer of single linked-list (glibc 2.32~).


### Syntax

```text
usage: heap calc-protected-fd [-h] [-b] fd LOCATION

positional arguments:
  fd             the fd value.
  LOCATION       the address to interpret as a chunk.

options:
  -h, --help     show this help message and exit
  -b, --as-base  use LOCATION as chunk base address (chunk_base_address = chunk_address - ptrsize * 2).
```

### Examples

```gdb
heap calc-protected-fd 0 0x5555555594e0
heap calc-protected-fd 0 0x5555555594e0 -b
```

## heap chunk

Display information on a heap chunk.

- Alias: `chunk`

### Syntax

```text
usage: heap chunk [-h] [-a ARENA_ADDR] [-b] LOCATION

positional arguments:
  LOCATION              the address to interpret as a chunk.

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -b, --as-base         use LOCATION as chunk base address (chunk_base_address = chunk_address - ptrsize * 2).
```

## heap chunks

Display information on all heap chunks.

- Alias: `chunks`

### Syntax

```text
usage: heap chunks [-h] [-a ARENA_ADDR] [-b NB_BYTE] [-o PEEK_OFFSET] [-n] [LOCATION]

positional arguments:
  LOCATION              the address interpreted as the beginning of a contiguous chunk. (default: arena.heap_base)

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -b, --nb-byte NB_BYTE
                        temporarily override `heap_chunks.peek_nb_byte`.
  -o, --peek-offset PEEK_OFFSET
                        temporarily override `heap_chunks.peek_offset`.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
heap chunks
heap chunks -a 0x7ffff0000020
heap chunks -a 1
```

### Notes

```text
about the annotation:
  - "tcache[idx=7,sz=0x90][1/2]"
    - idx: 0-origin index.
    - sz : the size of the chunk including metadata.
    - 1/ : a position in the free-list.
    -  /2: parsed free-list length including corrupted chunks.
           NOT the value of tcache_perthread_struct.count[idx], be careful!
  - "largebins[idx=98,sz=0x1000-0x1200][8/8]"
    - idx: 0-origin index that `i-th idx` means `bins[i*2 : (i+1)*2]`.
    - sz : the size range of the chunk including metadata.
    - 8/ : a position in the free-list. largebins are FIFO, so the last chunk will be used first.
    -  /8: parsed free-list length including corrupted chunks.
```

## heap dump-image

Visualize chunks on a heap as composition image.

- Alias: `dump-image`

### Syntax

```text
usage: heap dump-image [-h] [-a ARENA_ADDR] [-c MAX_COUNT] [-t] [-s] [-S SCALE] [-n] [LOCATION]

positional arguments:
  LOCATION           the address interpreted as the beginning of a contiguous chunk. (default: arena.heap_base)

options:
  -h, --help         show this help message and exit
  -a ARENA_ADDR      the address or number to interpret as an arena. (default: main_arena)
  -c MAX_COUNT       maximum number of chunks to parse; use when the number of chunks is very large.
  -t, --include-top  include top chunk.
  -s, --save-as-png  save as png.
  -S, --scale SCALE  magnification to enlarge or reduce the image.
  -n, --no-pager     do not use the pager.
```

### Notes

```text
[4mIn-use chunks[0m are displayed alternately in [38;2;125;125;125mdark gray[0m and [38;2;212;217;223mlight gray[0m.
[4mFreed chunks[0m are displayed alternately in [38;2;238;120;0mmuted red[0m and [38;2;255;243;82mmuted yellow[0m.
In both cases, the color is determined by whether the chunk's position from the beginning
is odd-numbered or even-numbered.

The `convert` command limits height to 32000px; output may shrink based on heap size.
```

## heap extract-heap-addr

Extract heap address from protected `fd` pointer of single linked-list (glibc 2.32~).


### Syntax

```text
usage: heap extract-heap-addr [-h] (--source | VALUE)

positional arguments:
  VALUE       the value to extract.

options:
  -h, --help  show this help message and exit
  --source    shows the source instead of displaying extracted value.
```

### Examples

```gdb
heap extract-heap-addr 0x000055500000C7F9
```

## heap find-fake-fast

Find candidate fake fast chunks from RW memory.


### Syntax

```text
usage: heap find-fake-fast [-h] [--include-heap] [--aligned] [--region-size-threshold REGION_SIZE_THRESHOLD] [-n] SIZE

positional arguments:
  SIZE                  search target size.

options:
  -h, --help            show this help message and exit
  --include-heap        heap is also included in the search target.
  --aligned             search only aligned chunks.
  --region-size-threshold REGION_SIZE_THRESHOLD
                        threshold for region size to skip search. (default: 0x2000000)
  -n, --no-pager        do not use the pager.
```

### Notes

```text
It is not possible to find candidates that straddle the two regions.
```

## heap parse

Display information on all heap chunks as Pwngdb style.

- Alias: `parseheap`

### Syntax

```text
usage: heap parse [-h] [-a ARENA_ADDR] [-n]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
heap parse
heap parse -a 0x7ffff0000020
heap parse -a 1
```

### Notes

```text
about the annotation:
  - "tcache[idx=7,sz=0x90][1/2]"
    - idx: 0-origin index.
    - sz : the size of the chunk including metadata.
    - 1/ : a position in the free-list.
    -  /2: parsed free-list length including corrupted chunks.
           NOT the value of tcache_perthread_struct.count[idx], be careful!
  - "largebins[idx=98,sz=0x1000-0x1200][8/8]"
    - idx: 0-origin index that `i-th idx` means `bins[i*2 : (i+1)*2]`.
    - sz : the size range of the chunk including metadata.
    - 8/ : a position in the free-list. largebins are FIFO, so the last chunk will be used first.
    -  /8: parsed free-list length including corrupted chunks.
```

## heap snapshot

Take a snapshot of heap.


### Syntax

```text
usage: heap snapshot [-h] [-a ARENA_ADDR] [--all]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  --all                 dump all arenas.
```

## heap snapshot-compare

Compare current heap with a previously saved heap-snapshot.


### Syntax

```text
usage: heap snapshot-compare [-h] [-a ARENA_ADDR] [-e] [-f] [-n] [-q] [FILE_PATH] [FILE_PATH2]

positional arguments:
  FILE_PATH             the filepath to compare (default: last dumped file).
  FILE_PATH2            the filepath to compare.

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -e, --extra           display extra chunk info.
  -f, --full            display after `top` chunk.
  -n, --no-pager        do not use the pager.
  -q, --quiet           quiet execution.
```

### Examples

```gdb
heap snapshot-compare /path/to/snapshot1                     # compare the current memory and file1
heap snapshot-compare /path/to/snapshot1 /path/to/snapshot2  # compare file1 and file2
```

### Notes

```text
Please specify the file obtained by the `heap snapshot` command.
Usually, it is saved in /tmp/gef/heap-snashot-arenaN-...
```

## heap tcache-index-helper

Helper for calculating tcache index etc.


### Syntax

```text
usage: heap tcache-index-helper [-h] [-a ARENA_ADDR] [-i INDEX] [-c COUNT_ADDR] [-e ENTRY_ADDR]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
  -i, --index INDEX     the index of tcache entry (0 ~ 63 (~glibc 2.41) or 75 (glibc 2.42~)).
  -c, --count-addr COUNT_ADDR
                        the address of &tcache.counts[i].
  -e, --entry-addr ENTRY_ADDR
                        the address of &tcache.entries[i].
```

## heap top

Display heap top chunk.

- Alias: `top-chunk`

### Syntax

```text
usage: heap top [-h] [-a ARENA_ADDR]

options:
  -h, --help            show this help message and exit
  -a, --arena-addr ARENA_ADDR
                        the address or number to interpret as an arena. (default: main_arena)
```

## heap tracer

Trace malloc/free to check heap integrity for UAF / Double-Free.

- Alias: `heap-analysis-helper`

### Syntax

```text
usage: heap tracer [-h] [-d] [-r]

options:
  -h, --help            show this help message and exit
  -d, --dump-current-list
                        show the tracked allocations.
  -r, --reset           remove breakpoints etc.
```

### Notes

```text
Note that splits and consolidates (which are performed inside `malloc` and `free`) are not tracked.
So this is not a strict trace.
```

## heap try-calloc

Emulate with unicorn to check errors when allocating a zero-initialized chunk.

- Alias: `try-calloc`

### Syntax

```text
usage: heap try-calloc [-h] [-a CALLER_ADDRESS] [-s] [-c COMMAND] [-v] SIZE NMEMB

positional arguments:
  SIZE                  the size to be allocated.
  NMEMB                 the number of blocks.

options:
  -h, --help            show this help message and exit
  -a, --calloc-addr CALLER_ADDRESS
                        the memory address of calloc().
  -s, --skip-emulation, --save
                        do not run, just save the script.
  -c, --command COMMAND
                        command to be executed after emulation succeeds, with the memory state temporarily reflected.
  -v, --verbose         show internal state.
```

### Examples

```gdb
heap try-calloc 0x10 1
heap try-calloc -a 0x7ffff7cae7a0 0x10 1    # need calloc address when no symbol
heap try-calloc -c "visual-heap" 0x10 1     # execute visual-heap
```

### Notes

```text
It may work even if NOT Glibc (untested).
It may be detected as a failure even though it actually succeeded.
  - Any system call was called
  - Any interrupt was raised
  - An instruction that unicorn does not support was executed
They are emulated to the best extent possible, but the emulation may be incomplete.
  - The address returned by mmap can differ from the actual one; this is an emulation limitation.
The failure message may not be detected because it is searched for heuristically.
```

## heap try-free

Emulate with unicorn to check errors when freeing a chunk.

- Alias: `try-free`

### Syntax

```text
usage: heap try-free [-h] [-a CALLER_ADDRESS] [-s] [-c COMMAND] [-v] ADDRESS

positional arguments:
  ADDRESS               the memory address to be freed.

options:
  -h, --help            show this help message and exit
  -a, --free-addr CALLER_ADDRESS
                        the memory address of free().
  -s, --skip-emulation, --save
                        do not run, just save the script.
  -c, --command COMMAND
                        command to be executed after emulation succeeds, with the memory state temporarily reflected.
  -v, --verbose         show internal state.
```

### Examples

```gdb
heap try-free 0x555555579930
heap try-free -a 0x7ffff7cadd30 0x555555579930    # need free address when no symbol
heap try-free -c "visual-heap" 0x555555579930     # execute visual-heap
```

### Notes

```text
It may work even if NOT Glibc (untested).
It may be detected as a failure even though it actually succeeded.
  - Any system call was called
  - Any interrupt was raised
  - An instruction that unicorn does not support was executed
They are emulated to the best extent possible, but the emulation may be incomplete.
  - The address returned by mmap can differ from the actual one; this is an emulation limitation.
The failure message may not be detected because it is searched for heuristically.
```

## heap try-malloc

Emulate with unicorn to check errors when allocating a chunk.

- Alias: `try-malloc`

### Syntax

```text
usage: heap try-malloc [-h] [-a CALLER_ADDRESS] [-s] [-c COMMAND] [-v] SIZE

positional arguments:
  SIZE                  the size to be allocated.

options:
  -h, --help            show this help message and exit
  -a, --malloc-addr CALLER_ADDRESS
                        the memory address of malloc().
  -s, --skip-emulation, --save
                        do not run, just save the script.
  -c, --command COMMAND
                        command to be executed after emulation succeeds, with the memory state temporarily reflected.
  -v, --verbose         show internal state.
```

### Examples

```gdb
heap try-malloc 0x120
heap try-malloc -a 0x7ffff7cad650 0x120    # need malloc address when no symbol
heap try-malloc -c "visual-heap" 0x120     # execute visual-heap
```

### Notes

```text
It may work even if NOT Glibc (untested).
It may be detected as a failure even though it actually succeeded.
  - Any system call was called
  - Any interrupt was raised
  - An instruction that unicorn does not support was executed
They are emulated to the best extent possible, but the emulation may be incomplete.
  - The address returned by mmap can differ from the actual one; this is an emulation limitation.
The failure message may not be detected because it is searched for heuristically.
```

## heap try-realloc

Emulate with unicorn to check errors when re-allocating a chunk.

- Alias: `try-realloc`

### Syntax

```text
usage: heap try-realloc [-h] [-a CALLER_ADDRESS] [-s] [-c COMMAND] [-v] ADDRESS SIZE

positional arguments:
  ADDRESS               the memory address to be re-allocated.
  SIZE                  the size to be re-allocated.

options:
  -h, --help            show this help message and exit
  -a, --realloc-addr CALLER_ADDRESS
                        the memory address of realloc().
  -s, --skip-emulation, --save
                        do not run, just save the script.
  -c, --command COMMAND
                        command to be executed after emulation succeeds, with the memory state temporarily reflected.
  -v, --verbose         show internal state.
```

### Examples

```gdb
heap try-realloc 0x555555579930 0x120
heap try-realloc -a 0x7ffff7cae0a0 0x555555579930 0x120    # need realloc address when no symbol
heap try-realloc -c "visual-heap" 0x555555579930 0x120     # execute visual-heap
```

### Notes

```text
It may work even if NOT Glibc (untested).
It may be detected as a failure even though it actually succeeded.
  - Any system call was called
  - Any interrupt was raised
  - An instruction that unicorn does not support was executed
They are emulated to the best extent possible, but the emulation may be incomplete.
  - The address returned by mmap can differ from the actual one; this is an emulation limitation.
The failure message may not be detected because it is searched for heuristically.
```

## heap visual-heap

Visualize chunks on a heap.

- Alias: `visual-heap`

### Syntax

```text
usage: heap visual-heap [-h] [-a ARENA_ADDR] [-c MAX_COUNT] [-f] [-d] [-s] [-n] [LOCATION]

positional arguments:
  LOCATION              the address interpreted as the beginning of a contiguous chunk. (default: arena.heap_base)

options:
  -h, --help            show this help message and exit
  -a ARENA_ADDR         the address or number to interpret as an arena. (default: main_arena)
  -c MAX_COUNT          maximum number of chunks to parse; use when the number of chunks is very large.
  -f, --full            display the same line without omitting.
  -d, --dark-color      use the dark color if chunk is allocated.
  -s, --safe-linking-decode
                        decode safe-linking encoded pointer if tcache or fastbins.
  -n, --no-pager        do not use the pager.
```

# 05-b. Heap - Chromium/V8
## cage

Display v8 (Chromium and d8) ubercage area.


### Syntax

```text
usage: cage [-h] [-f] [-v] [-vv] [-vvv] [-n] [LOCATION]

positional arguments:
  LOCATION              the address for filtering.

options:
  -h, --help            show this help message and exit
  -f, --force-heuristic
                        use heuristic detection.
  -v, --verbose         show with zero page.
  -vv, --vverbose       show with permission NONE.
  -vvv, --vvverbose     show all maps (=~ vmmap).
  -n, --no-pager        do not use the pager.
```

## partition-alloc-dump

PartitionAlloc free-list viewer for chromium stable.


### Syntax

```text
usage: partition-alloc-dump [-h] [-f] [-r ROOT] [-n] [-v] [--debug] {fast_malloc,array_buffer,buffer,fm,ab,b}

positional arguments:
  {fast_malloc,array_buffer,buffer,fm,ab,b}
                        the target buffer_root. The last three are abbreviated forms.

options:
  -h, --help            show this help message and exit
  -f, --force-heuristic
                        use heuristic roots detection.
  -r, --root ROOT       the memory address of target {buffer,array_buffer,fast_malloc}_root_.
  -n, --no-pager        do not use the pager.
  -v, --verbose         display also empty slots.
  --debug               [FOR DEVELOPER] enable debug print.
```

### Examples

```gdb
partition-alloc-dump array_buffer  # walk from array_buffer_root_
partition-alloc-dump ab            # same above
```

### Notes

```text
Chromium mainline is too fast to develop. So if parse is failed, you need fix this gef.py.

Simplified partition alloc structure:

+-root-----------------+
| ...                  |    +---->+-extent------------+  +-->+-extent------------+  +-> ...
| next_super_page_     |    |     | next              |--+   | next              |--+
| next_partition_page_ |    |     +-------------------+      +-------------------+
| ...                  |    |
| first_extent_        |----+
| direct_map_list_     |--------->+-direct_map_extent-+  +-->+-direct_map_extent-+  +-> ...
| ...                  |          | bucket            |  |   | bucket            |  |
|                      |          | next_extent       |--+   | next_extent       |--+
|                      |          +-------------------+      +-------------------+
|                      |
+-bucket[0](0x20)------+
| head                 |--------->+-slot_span---------+  +-->+-slot_span---------+  +-> ...
| slot_size            |<---------| bucket            |  |   | bucket            |  |
| ...                  |    +-----| freelist_head     |  |   | freelist_head     |  |
+-bucket[1](0x20)------+    |     | next_slot_span    |--+   | next_slot_span    |--+
| head                 |    |     +-------------------+      +-------------------+
| slot_size            |    |
| ...                  |    |
+----------------------+    +---->+-slot--------------+
| ...                  |          | next              |---+
|                      |          | (freed)           |   |
+----------------------+          +-slot--------------+   |
                                  |                   |   |
                                  | (used)            |   |
                                  +-slot--------------+<--+
                              +---| next              |
                              |   | (freed)           |
                              |   +-slot--------------+
                              |   |                   |
                              |   | (used)            |
                              +-->+-slot--------------+
                                  | next              |---> NULL
                                  | (freed)           |
                                  +-slot--------------+
                                  |                   |
                                  |                   |
                                  +-------------------+

`extent`, `slot_span` and `slot` are in super_page.

     [~v144.x]                    [v145.x~; PA_CONFIG(MOVE_METADATA_OUT_OF_GIGACAGE)=y]
     +-super_page-(2MB)-----+      +-super_page(for meta)-+ +-super_page(for chunk)+
4KB  | Guard Page           |      | Guard Page           | | Guard Page           |
     +----------------------+      +----------------------+ +----------------------+
4KB  | extent * 1           |      | extend * 1           | | Unused               |
     | slot_span * 126      |      | slot_span * 126      | |                      |
     | unused * 1           |      | unused * 1           | |                      |
     +----------------------+      +----------------------+ +----------------------+
8KB  | Guard Page           |      | Guard Page           | | Guard Page           |
     +----------------------+      +----------------------+ +----------------------+
16KB | Partition Page #1    |      | ...                  | | Partition Page #1    |
     |   slot               |      |                      | |   slot               |
     |   slot               |      |                      | |   slot               |
     |   ...                |      |                      | |   ...                |
     +----------------------+      |                      | +----------------------+
     | ...                  |      |                      | | ...                  |
     +----------------------+      |                      | +----------------------|
16KB | Partition Page #126  |      |                      | | Partition Page #126  |
     |   slot               |      |                      | |   slot               |
     |   slot               |      |                      | |   slot               |
     |   ...                |      |                      | |   ...                |
     +----------------------+      +----------------------+ +----------------------+
12KB | Unused               |      | Unused               | | Unused               |
     +----------------------+      +----------------------+ +----------------------+
 4KB | Guard Page           |      | Guard Page           | | Guard Page           |
     +----------------------+      +----------------------+ +----------------------+

                                   * super_page_for_meta - metadata_offset_ == super_page_for_chunk
```

## v8

Print v8 tagged object, or load more commands from internet.


### Syntax

```text
usage: v8 [-h] (-l | -L | ADDRESS)

positional arguments:
  ADDRESS               target map address.

options:
  -h, --help            show this help message and exit
  -l, --load-v8-gdbinit
                        load gdbinit for v8 from internet.
  -L, --list-command    show newly added commands from v8 gdbinit.
```

## v8-dump-space

Dump v8 (Chromium and d8) heap objects in each space.


### Syntax

```text
usage: v8-dump-space [-h] [-m MAX_COUNT] [-n] [-v] [-vv] [TARGET_SPACE]

positional arguments:
  TARGET_SPACE          the space name to dump.

options:
  -h, --help            show this help message and exit
  -m, --max-count MAX_COUNT
                        max count for each space.
  -n, --no-pager        do not use the pager.
  -v, --verbose         display also object details for string like objects (slow!).
  -vv, --vverbose       display also object details for all objects (very slow!).
```

### Notes

```text
It only works with the debug build of d8 or Chromium.
Since many parts are detected heuristically and testing is insufficient,
it is highly likely that it will not work depending on the version of v8.
```

## v8-list-maps

List v8 (Chromium and d8) built-in maps.


### Syntax

```text
usage: v8-list-maps [-h] [-hh] [-r] [-n]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -r, --rescan        do not use map cache.
  -n, --no-pager      do not use the pager.
```

### Notes

```text
Simplified built-in maps structure:

                             +-cage-------------+
chromium: partition-alloc    | +-ro_space-----+ |
+-d8: glibc-heap-+           | | ...          | |
| ...            |           | | ...          | |
| *map           |------------>| map          | |
| *map           |------------>| map          | |
| *map1          |------------>| map1         |<----+
| *map           |------------>| map          | |   |
| *map           |------------>| map          | |   |
| ...            |           | | ...          | |   + cage_base
+----------------+           | | ...          | |   |
                             | +-old_space----+ |   |
                             | | ...          | |   |
                             | | +0x10: ofs   |-----+
                             | | ...          | |
                             | +--------------+ |
                             | | ...          | |
                             | +--------------+ |
                             | | ...          | |
                             | +--------------+ |
                             | ...              |
                             +------------------+

For Chromium: this command needs `--no-sandbox` to bypass `seccomp`.
Also, since it uses V8 commands internally, `_v8_internal_Print_Object` must be resolvable.
```

# 05-c. Heap - Other
## go-heap-dump

go language v1.24.4 mheap dumper (x64 only).


### Syntax

```text
usage: go-heap-dump [-h] [-hh] [--mheap MHEAP] [--mspan MSPAN] [-d] [-n] [-v]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  --mheap MHEAP       the address of runtime.mheap_.
  --mspan MSPAN       the address of the target mspan.
  -d, --dump          with hexdump.
  -n, --no-pager      do not use the pager.
  -v, --verbose       display also empty slots.
```

### Notes

```text
Simplified Go heap structure:

+-runtime.mheap_-+
| ...            |
| allspans       |
|  array         |--->+-mspan*[]--+
|  len           |    | [0]       |----+
|  cap           |    | [1]       |----|----+
| ...            |    | ...       |    |    |
| arenas         |    +-----------+    |    |
| ...            |                     |    |
| central        |                     |    |
| ...            |                     |    |
+----------------+                     |    |
                                       |    v
 +-------------------------------------+   ...
 |
 v
+-mspan-------+         +-mspan-------+
| next        |-------->| next        |-------->...
| prev        |<--------| prev        |<--------...
| startAddr   |---+     | startAddr   |---+
| npages      |   |     | npages      |   |
| nelems      |   |     | nelems      |   |
| allocBits   |---|--+  | allocBits   |---|--+
| spanClass   |   |  |  | spanClass   |   |  |
+-------------+   |  |  +-------------+   |  |
                  |  v                    |  v
                  | +-gcBits------+       | +-gcBits------+
                  | | bit[0]      |       | | bit[0]      |
                  | | bit[1]      |       | | bit[1]      |
                  | | ...         |       | | ...         |
                  | +-------------+       | +-------------+
                  v                       v
                +-object-+ +-object-+   +-object-+ +-object-+
                | chunk  | | chunk  |   | chunk  | | chunk  |
                +--------+ +--------+   +--------+ +--------+

* `allspans` is used as the entry point for this command.
* `spanClass >> 1` is used as the size class, and the size class is converted to chunk size.
* `allocBits` is used to distinguish allocated/free objects in a span.
* `arenas`, `central`, and walking from `mspan.next` are currently unsupported.
```

## hoard-heap-dump

Hoard v3.2 (2025/12/31) heap free-list viewer (x64 only).


### Syntax

```text
usage: hoard-heap-dump [-h] [-hh] [-b SUPERBLOCK] [-n]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -b, --superblock SUPERBLOCK
                        the address of superblock.
  -n, --no-pager        do not use the pager.
```

### Notes

```text
Simplified Hoard structure:

                                  +-SmallHeap-+
                                  | ...       |
                                  +-----------+
                                        ^
                                        |
     +-superblock-------------------+   |      +-superblock--+   +-superblock--+
     | vtable                       |   |      | vtable      |   | vtable      |
     | magic                        |   |      | magic       |   | magic       |
     | objectSize                   |   |      | objectSize  |   | objectSize  |
     | totalObjects                 |   |      | ...         |   | ...         |
     | owner                        |---+      | prev        |<->| prev        |<-> ...
...<-> prev                         |<-------->| next        |   | next        |
     | next                         |--------->| ...         |   | ...         |
     | reapableObjects              |          | freeList    |   | freeList    |
     | objectsFree                  |          | start       |   | start       |
     | start                        |--+       | position    |   | position    |
     | position                     |  |       +-------------+   +-------------+
     | freeList                     |--|--+
     +------------------------------+  |  |
                                       |  |       [free object freelist]
                                       |  |        +-object--+  +-object--+
                                       |  +------->| next    |->| next    |->NULL
                                       |           +---------+  +---------+
                                       |
                                       |          [unused objects]
                                       |           +-object--+  +-object--+
                                       +---------->|         |  |         |  ...
                                                   +---------+  +---------+

* This command scans anonymous writable mappings and detects superblocks by vtable and magic.
* `--superblock` can be used to specify superblocks manually.
* `_freeList` is used first; if it is empty, TLS-held freelist heads are searched as candidates.
* Before allocating from the freelist, Hoard consumes unused objects from `position`.
* `reapableObjects` is displayed as the number of unused objects left.
```

## mimalloc-heap-dump

mimalloc heap free-list viewer (x64 only).


### Syntax

```text
usage: mimalloc-heap-dump [-h] [-hh] [-m MI_HEAP_MAIN] [-D] [-n]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -m, --mi-heap-main MI_HEAP_MAIN
                        the address of _mi_heap_main (v2.x) / heap_main (v3.x).
  -D, --dump-chunk      dump each chunks.
  -n, --no-pager        do not use the pager.
```

### Notes

```text
Simplified mimalloc structure:

+-mi_heap_t(_mi_heap_main / heap_main)-+
| ...                                  |
| next                                 |----> mi_heap_t --> ...
| pages_free_direct[130] (v2.x/v3.0.x) |------+
| theap / theaps (v3.1.x~)             |---+  |
+--------------------------------------+   |  |
                                           |  |
  +----------------------------------------+  |
  |                                           |
  v                                           |
+-mi_theap_t(v3.1.x~)------------------+      |
| heap                                 |      |
| ...                                  |      |
| tnext / hnext                        |      |
| pages_free_direct[130]               |------+
| pages[]                              |      |
+--------------------------------------+      |
                                              |
  +-------------------------------------------+
  |
  v
+-mi_page_t-------------+               +-block-+  +-block-+
| capacity              |       +------>| next  |->| next  |->...
| used                  |       |       +-------+  +-------+
| block_size/xblock_size|       |
| page_start (v2.1.3~)  |---+   |       [page blocks]
| keys[0]               |   |   |       +-block-+  +-block-+
| keys[1]               |   +---------->|       |  |       | ...
| free                  |-------+       +-------+  +-------+
| local_free            |-------+
| xthread_free          |       |       +-block-+  +-block-+
| xheap / theap / heap  |       +------>| next  |->| next  |->...
| next                  |               +-------+  +-------+
| prev                  |
+-----------------------+

* In mimalloc, the member offsets of important structures vary depending on the version.
* You should be able to check the version with a command like `strings libmimalloc.so | grep git`.
* If you cannot determine it, please choose an option that can successfully decode it.

* For `_mi_heap_main` (v2.x) or `heap_main` (v3.x), GEF tries to resolve the address from symbol.
* If symbols are not available, GEF scans the TLS area for automatic detection.
```

## musl-heap-dump

musl v1.2.5 (src/malloc/mallocng) heap reusable chunks viewer (x64/x86 only).


### Syntax

```text
usage: musl-heap-dump [-h] [-i ACTIVE_IDX] [-n] [-v] [{ctx,unused}]

positional arguments:
  {ctx,unused}          dump mode (default: unused).

options:
  -h, --help            show this help message and exit
  -i, --active-idx ACTIVE_IDX
                        the active index of dump target.
  -n, --no-pager        do not use the pager.
  -v, --verbose         also dump an empty active index.
```

## scalloc-heap-dump

scalloc heap free-list viewer (x64 only).


### Syntax

```text
usage: scalloc-heap-dump [-h] [-hh] [--object_space OBJECT_SPACE] [-n]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  --object_space OBJECT_SPACE
                        use specific address for object_space.
  -n, --no-pager        do not use the pager.
```

### Notes

```text
Simplified scalloc structure:

+-Arena(object_space)-+
| name_               |--->"object"
| start_              |------+
| end_                |------|---->Span[N]
| len_                |      |
| current_            |------|---->Span[i]
+---------------------+      |
                             |
  +--------------------------+
  v
+-Span[0]-------------+                +-Span[1]-------------+
| span_link_.next_    |--------------->| span_link_.next_    |---->...
| span_link_.prev_    |<---------------| span_link_.prev_    |<----...
| owner_              |                | owner_              |
| epoch_              |                | epoch_              |
| size_class_         |                | size_class_         |
| local_free_list_    |-----+          | local_free_list_    |-----+
| remote_free_list_   |--+  |          | remote_free_list_   |--+  |
+---------------------+  |  |          +---------------------+  |  |
                         |  |                                   |  |
   +---------------------+  |             +---------------------+  |
   |                        |             |                        |
   |  +---------------------+             |  +---------------------+
   |  |                                   |  |
   |  |  +-object-+   +-object-+          |  |  +-object-+   +-object-+
   |  +->| next   |-->| next   |-->...    |  +->| next   |-->| next   |-->...
   |     +--------+   +--------+          |     +--------+   +--------+
   |                                      |
   |     +-object-+   +-object-+          |     +-object-+   +-object-+
   +---->| next   |-->| next   |-->...    +---->| next   |-->| next   |-->...
         +--------+   +--------+                +--------+   +--------+

* `object_space` is used as the default arena pointer.
* Spans are walked from `Arena.start_` to `Arena.current_` by `kVirtualSpanSize`.
* `size_class_` is converted to object size and capacity by fixed tables.
* `local_free_list_.list_` points to the local free-list.
* `local_free_list_.bump_pointer_` points to the next unused object area (top).
* `remote_free_list_.top_` is a tagged pointer and is decoded before dumping.
```

## snmalloc-heap-dump

snmalloc (as of June 2025) heap free-list viewer (x64 only).


### Syntax

```text
usage: snmalloc-heap-dump [-h] [-a] [-l] [-r] [-n] [-v]

options:
  -h, --help      show this help message and exit
  -a, --all       dump all thread_alloc.
  -l, --laden     dump laden (large or inactive slabs).
  -r, --remote    dump remote_alloc (WIP).
  -n, --no-pager  do not use the pager.
  -v, --verbose   display also empty freelists.
```

### Notes

```text
This command dumps the following four categories:
- small_fast_free_lists: Free list per small size class (fast path).
- alloc_classes: Per size class list of active slabs.
- laden: The set of all slabs and large allocations from this allocator that are full or almost full.
    - The end of the list may not be dumped correctly.
- remote_alloc: Message queue for allocations being returned to this allocator.
    - Currently status: WIP.
```

## ssmalloc-heap-dump

SSMalloc heap free-list viewer (x64 only).


### Syntax

```text
usage: ssmalloc-heap-dump [-h] [-hh] [--local_heap LOCAL_HEAP] [--global_pool GLOBAL_POOL] [-a] [-g] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  --local_heap LOCAL_HEAP
                        use specific address for local_heap.
  --global_pool GLOBAL_POOL
                        use specific address for global_pool.
  -a, --all             dump all local_heap.
  -g, --global          dump global_pool queues.
  -n, --no-pager        do not use the pager.
  -v, --verbose         display also empty freelists.
```

### Notes

```text
Simplified SSMalloc structure:

+-lheap_t(local heap)------------------+
| free_head (completely free dchunks)  |------> dchunk_t --> dchunk_t --> ...
| foreground[] (active dchunk)         |---+
| background[] (non-full dchunks)      |<--|--> dchunk_t <-> dchunk_t <-> ...
| block_bufs[] (remote-free buffer)    |   |
| need_gc[] (remote-free dchunks)      |   |
+--------------------------------------+   |
                                           |
  +----------------------------------------+
  |
  v                                    [local free objects]
+-dchunk_t-------------+               +-object-+  +-object-+
| ...                  |       +------>| next   |->| next   |->...
| size_cls             |       |       +--------+  +--------+
| ...                  |       |
| free_head            |-------+       [unused / bump area]
| block_size           |               +-object-+  +-object-+
| free_mem             |-------------->|        |  |        |...
| remote_free_head     |-------+       +--------+  +--------+
+----------------------+       |
                               |       [remote free objects]
                               |       +-object-+  +-object-+
                               +------>| next   |->| next   |->...
                                       +--------+  +--------+

* `local_heap` is the per-thread entry point.
* `lheap_t.free_head` is completely free chunks kept by the local heap.
* `lheap_t.foreground[size_cls]` points to the active `dchunk_t` for that size class.
* `lheap_t.background[size_cls]` is a doubly linked list of non-full dchunks.
* `dchunk_t.free_head` is locally freed objects.
* Allocation from a `dchunk_t` pops `free_head` first; if it is empty, allocation advances `free_mem`.
```

## tcmalloc-dump

tcmalloc (google-perftools/gperftools) free-list viewer (x64 only).


### Syntax

```text
usage: tcmalloc-dump [-h] [-hh] [-c] [-f] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -c, --central         show central cache instead of thread caches.
  -f, --force-heuristic
                        use heuristic detection.
  -n, --no-pager        do not use the pager.
  -q, --quiet           quiet mode.
```

### Examples

```gdb
tcmalloc-dump            # print freelist of thread cache for all thread
tcmalloc-dump --central  # print freelist of central cache
```

### Notes

```text
Simplified tcmalloc/gperftools heap structure:

Static Area (Central Cache)
+------------------------------+
| Static::sizemap_             |
|  class_to_size_[class]       |
+------------------------------+
| Static::central_cache_[128]  |
|  CentralFreeList[class]      |
|   empty_ / nonempty_         |
|   tc_slots_[slot].head       |---> free obj -> free obj -> NULL
|   used_slots_                |
+------------------------------+
| Static::pageheap_            |
+------------------------------+

Thread cache list
+----------------------------+  +-->+-ThreadCache---------+       +-ThreadCache---------+
| ThreadCache::thread_heaps_ |--+   | list_[128]          |    +->| list_[128]          |    +-> ...
+----------------------------+      |  FreeList::list_    |--+ |  |  FreeList::list_    |--+ |
                                    |  FreeList::length_  |  | |  |  FreeList::length_  |  | |
                                    |  FreeList::size_    |  | |  |  FreeList::size_    |  | |
                                    | next_               |----+  | next_               |----+
                                    | prev_               |  |    | prev_               |  |
                                    +---------------------+  |    +---------------------+  |
                                                             v                             v
                                                         free obj -> free obj -> NULL     ...
```

## tlsf-heap-dump

TLSF (Two-Level Segregated Fit) v2.4.6 free-list viewer (x64 only).


### Syntax

```text
usage: tlsf-heap-dump [-h] [-hh] [--pool POOL] [-n] [-v]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  --pool POOL         the address of memory pool.
  -n, --no-pager      do not use the pager.
  -v, --verbose       display also empty slots.
```

### Notes

```text
Simplified TLSF structure:

+-TLSF_struct------+
| tlsf_signature   |
| lock             |
| used_size        |
| max_size         |     +-area_info_t-+    +-area_info_t-+
| area_head        |---->| next        |--->| next        |->...
| fl_bitmap        |     | end         |    | end         |
| sl_bitmap[]      |     +-------------+    +-------------+
| matrix[][]       |---+
+------------------+   |
                       | matrix[fl][sl]
                       |
                       +--->+-bhdr_t------+    +-bhdr_t------+
                            | prev_hdr    |    | prev_hdr    |
                            | size        |    | size        |
                       ...<-| prev        |<---| prev        |
                            | next        |--->| next        |->...
                            +-------------+    +-------------+

* `mp` is used as the default pool pointer.
* `--pool` can be used to specify a TLSF pool (arena_info_t) manually.
* `fl_bitmap` and `sl_bitmap[]` show which free-list classes are non-empty.
* `matrix[fl][sl]` points to a doubly linked free-list of `bhdr_t` chunks.
* Allocated chunks are not linked from `matrix[][]`, so this command dumps free chunks only.
```

## uclibc-ng-heap-dump

uclibc-ng (libc/stdlib/malloc-standard) heap reusable chunks viewer (x64/x86 only).


### Syntax

```text
usage: uclibc-ng-heap-dump [-h] [--malloc_state MALLOC_STATE] [-n] [-v]

options:
  -h, --help            show this help message and exit
  --malloc_state MALLOC_STATE
                        use specific address for malloc_context.
  -n, --no-pager        do not use the pager.
  -v, --verbose         also dump an empty active index.
```

### Notes

```text
The main structural differences between uclibc-ng (malloc-standard) and glibc are:
- No tcache. There are fastbins, an unsorted bin, small bins, and large bins.
- No thread arena. Therefore, chunks do not have the NON_MAIN_ARENA flag.
The structure of malloc-standard has remained largely unchanged from version 1.0 to the latest.
As a result, it should be usable with any version.
Since the final version of uclibc (not uclibc-ng) uses the same structure,
this command should also be usable with uclibc.
```

## uclibc-ng-visual-heap

Visualize chunks on a heap for uClibc-ng.


### Syntax

```text
usage: uclibc-ng-visual-heap [-h] [--malloc_state MALLOC_STATE] [-c MAX_COUNT] [-f] [-d] [-s] [-n] [LOCATION]

positional arguments:
  LOCATION              the address interpreted as the beginning of a contiguous chunk. (default: [heap] of vmmap)

options:
  -h, --help            show this help message and exit
  --malloc_state MALLOC_STATE
                        use specific address for malloc_context.
  -c MAX_COUNT          Maximum count to parse. It is used when there is a very large amount of chunks.
  -f, --full            display the same line without omitting.
  -d, --dark-color      use the dark color if chunk is allocated.
  -s, --safe-linking-decode
                        decode safe-linking encoded pointer if tcache or fastbins.
  -n, --no-pager        do not use the pager.
```

### Notes

```text
The main structural differences between uclibc-ng (malloc-standard) and glibc are:
- No tcache. There are fastbins, an unsorted bin, small bins, and large bins.
- No thread arena. Therefore, chunks do not have the NON_MAIN_ARENA flag.
The structure of malloc-standard has remained largely unchanged from version 1.0 to the latest.
As a result, it should be usable with any version.
Since the final version of uclibc (not uclibc-ng) uses the same structure,
this command should also be usable with uclibc.
```

# 06-a. Qemu-system/KGDB Cooperation - Memory Map
## kvmmap

Print kernel memory map.

- Alias: `pagewalk-with-hints`

### Syntax

```text
usage: kvmmap [-h] [-U] [-i] [-v] [-n] [-q] [ADDRESS ...]

positional arguments:
  ADDRESS               filtering by specified address.

options:
  -h, --help            show this help message and exit
  -U, --exclude-user    exclude userland memory.
  -i, --include-esp-fixup-stacks
                        include `%esp fixup stacks` area (sometimes heavy memory use; x64 only).
  -v, --verbose         increase output verbosity. (-v, -vv, -vvv)
  -n, --no-pager        do not use the pager.
  -q, --quiet           quiet execution.
```

## pagewalk

The base command to dump page tables.

- Alias: `pw`, `ptdump`, `pt`

### Syntax

```text
usage: pagewalk [-h] {x64,x86,arm,arm64,riscv} ...

options:
  -h, --help            show this help message and exit

command:
  {x64,x86,arm,arm64,riscv}
```

## pagewalk arm

Dump pagetable for ARM Cortex-A. PL2 pagewalk is unsupported.

- Alias: `pagewalk arm32`

### Syntax

```text
usage: pagewalk arm [-h] [-S | -s] [-L] [-N] [-P] [-Q] [-f REGEX] [-v VADDR] [-p PADDR] [-t VADDR] [--optee] [-D] [-c] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -S                    use TTBRn_ELm_S to parse start.
  -s                    use TTBRn_ELm to parse start.
  -L, --print-each-level
                        show all level pagetables.
  -N, --no-merge        do not merge similar/consecutive address.
  -P, --sort-by-phys    sort by physical address.
  -Q, --simple          merge with ignoring physical address consecutivness.
  -f, --filter REGEX    filter by REGEX pattern.
  -v, --vrange VADDR    filter by map included specified virtual address.
  -p, --prange PADDR    filter by map included specified physical address.
  -t, --trace VADDR     show all level pagetables only associated specified address.
  --optee               show the secure world memory maps if used OP-TEE.
  -D, --disable-color   disable RWX colored output
  -c, --use-cache       use previous result.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

## pagewalk arm64

Dump pagetable for ARM64 Cortex-A (ARM v8.7 base).


### Syntax

```text
usage: pagewalk arm64 [-h] [-L] [-N] [-P] [-Q] [-f REGEX] [-v VADDR] [-p PADDR] [-t VADDR] [--optee] [-0] [-1] [-D] [-c] [-n] [-q] [TARGET_EL]

positional arguments:
  TARGET_EL             target Exception Level. (default: current EL)

options:
  -h, --help            show this help message and exit
  -L, --print-each-level
                        show all level pagetables.
  -N, --no-merge        do not merge similar/consecutive address.
  -P, --sort-by-phys    sort by physical address.
  -Q, --simple          merge with ignoring physical address consecutivness.
  -f, --filter REGEX    filter by REGEX pattern.
  -v, --vrange VADDR    filter by map included specified virtual address.
  -p, --prange PADDR    filter by map included specified physical address.
  -t, --trace VADDR     show all level pagetables only associated specified address.
  --optee               show the secure world memory maps if used OP-TEE.
  -0, --only-TTBR0_EL1  Display only TTBR0_EL1 (if target==EL1)
  -1, --only-TTBR1_EL1  display only TTBR1_EL1 (if target==EL1)
  -D, --disable-color   disable RWX colored output
  -c, --use-cache       use previous result.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

## pagewalk riscv

Dump pagetable for riscv64/32.

- Alias: `pagewalk riscv32`, `pagewalk riscv64`

### Syntax

```text
usage: pagewalk riscv [-h] [-L] [-N] [-P] [-Q] [-f REGEX] [-v VADDR] [-p PADDR] [-t VADDR] [-D] [-c] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -L, --print-each-level
                        show all level pagetables.
  -N, --no-merge        do not merge similar/consecutive address.
  -P, --sort-by-phys    sort by physical address.
  -Q, --simple          merge with ignoring physical address consecutivness.
  -f, --filter REGEX    filter by REGEX pattern.
  -v, --vrange VADDR    filter by map included specified virtual address.
  -p, --prange PADDR    filter by map included specified physical address.
  -t, --trace VADDR     show all level pagetables only associated specified address.
  -D, --disable-color   disable RWX colored output
  -c, --use-cache       use previous result.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

## pagewalk x64

Dump pagetable for x64/x86.

- Alias: `pagewalk x86`

### Syntax

```text
usage: pagewalk x64 [-h] [-L] [-N] [-P] [-Q] [-f REGEX] [-v VADDR] [-p PADDR] [-t VADDR] [-i] [-U] [--cr3 USER_SPECIFIED_CR3] [--cr4 USER_SPECIFIED_CR4] [--ept] [-D] [-c] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -L, --print-each-level
                        show all level pagetables.
  -N, --no-merge        do not merge similar/consecutive address.
  -P, --sort-by-phys    sort by physical address.
  -Q, --simple          merge with ignoring physical address consecutivness.
  -f, --filter REGEX    filter by REGEX pattern.
  -v, --vrange VADDR    filter by map included specified virtual address.
  -p, --prange PADDR    filter by map included specified physical address.
  -t, --trace VADDR     show all level pagetables only associated specified address.
  -i, --include-esp-fixup-stacks
                        include `%esp fixup stacks` area (sometimes heavy memory use; x64 only).
  -U, --user-pt         print userland pagetables (for KPTI, x64 only, in kernel context).
  --cr3 USER_SPECIFIED_CR3
                        use specified value as cr3.
  --cr4 USER_SPECIFIED_CR4
                        use specified value as cr4.
  --ept                 parse cr3 as EPT (Extended Page Table).
  -D, --disable-color   disable RWX colored output
  -c, --use-cache       use previous result.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

# 06-b. Qemu-system/KGDB Cooperation - Register
## cet

Display Intel CET settings.


### Syntax

```text
usage: cet [-h]

options:
  -h, --help  show this help message and exit
```

## gdtinfo

Print GDT/LDT entries. If user-land, show sample entries.


### Syntax

```text
usage: gdtinfo [-h] [--only-gdt] [--only-ldt] [-q] [-v] [-n]

options:
  -h, --help      show this help message and exit
  --only-gdt      show only GDT entries (qemu-system only).
  --only-ldt      show only LDT entries (qemu-system only).
  -q, --quiet     enable quiet mode.
  -v, --verbose   also display bit information of gdt entries.
  -n, --no-pager  do not use the pager.
```

### Notes

```text
This command is intended to dump the GDTR and LDTR when working with qemu-system.
When you're debugging a normal userland app you can't read the GDTR or LDTR,
so this is just to show you an example of what information is stored there.
However, the segment registers show the correct (real) values.
```

## idtinfo

Print IDT entries. If user-land, show sample entries.


### Syntax

```text
usage: idtinfo [-h] [-q] [-v] [-n]

options:
  -h, --help      show this help message and exit
  -q, --quiet     enable quiet mode.
  -v, --verbose   also display bit information of idt entries.
  -n, --no-pager  do not use the pager.
```

### Notes

```text
This command is intended to dump the IDTR when working with qemu-system.
When you're debugging a normal userland app you can't read the IDTR,
so this is just to show you an example of what information is stored there.
```

## msr

Read or write MSR value.


### Syntax

```text
usage: msr [-h] [-q] [MSR_NAME|MSR_CONST] [MSR_VALUE]

positional arguments:
  MSR_NAME|MSR_CONST  the MSR name or constant to know the value.
  MSR_VALUE           the MSR value to update.

options:
  -h, --help          show this help message and exit
  -q, --quiet         quiet mode.
```

### Examples

```gdb
msr                   # show frequently used MSRs
msr 0xc0000080        # read msr
msr MSR_EFER          # another valid format
msr 0xc0000080 0xd01  # write msr
```

### Notes

```text
Disable `-enable-kvm` option for qemu-system.
```

## qreg

Get registers via qemu-monitor and show the detail of x64/x86 system registers.


### Syntax

```text
usage: qreg [-h] [-v] [-n]

options:
  -h, --help      show this help message and exit
  -v, --verbose   also display detailed bit information.
  -n, --no-pager  do not use the pager.
```

## read-system-register-for-kgdb

Read system register for kgdb / kdb.


### Syntax

```text
usage: read-system-register-for-kgdb [-h] (-l | REGISTER_NAME)

positional arguments:
  REGISTER_NAME  register name to read a value.

options:
  -h, --help     show this help message and exit
  -l, --list     show the supported register names.
```

### Examples

```gdb
read-system-register-for-kgdb cr0
read-system-register-for-kgdb TTBR0_EL1
```

## read-system-register-for-qemu-arm

Read system register for old qemu-system-arm.


### Syntax

```text
usage: read-system-register-for-qemu-arm [-h] REGISTER_NAME

positional arguments:
  REGISTER_NAME  register name to read a value.

options:
  -h, --help     show this help message and exit
```

### Examples

```gdb
read-system-register-for-qemu-arm TTBR0
```

### Notes

```text
Attempting to read a non-existing register raises an undefined exception.
```

## switch-el

Switch EL (Exception Level) on ARM64 architecture.


### Syntax

```text
usage: switch-el [-h] [TARGET_EL]

positional arguments:
  TARGET_EL   Exception Level to change to.

options:
  -h, --help  show this help message and exit
```

## vbar

Pretty-print ARM/ARM64 vector table.


### Syntax

```text
usage: vbar [-h] [-a ADDRESS] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        the vector address.
  -n, --no-pager        do not use the pager.
  -v, --verbose         display all instructions (for ARM64).
```

# 06-c. Qemu-system/KGDB Cooperation - Linux Basic
## kbase

Display kernel base address.


### Syntax

```text
usage: kbase [-h] [-r] [-q]

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
  -q, --quiet   enable quiet mode.
```

## kchecksec

Check the security properties of the current kernel.


### Syntax

```text
usage: kchecksec [-h]

options:
  -h, --help  show this help message and exit
```

## kcmdline

Display kernel command-line string.


### Syntax

```text
usage: kcmdline [-h] [-r] [-q]

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
  -q, --quiet   enable quiet mode.
```

## kcurrent

Display current task.


### Syntax

```text
usage: kcurrent [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  enable quiet mode.
```

## kmagic

Display useful kernel addresses and offsets.


### Syntax

```text
usage: kmagic [-h] [FILTER ...]

positional arguments:
  FILTER      filter string.

options:
  -h, --help  show this help message and exit
```

## kversion

Display kernel version string.


### Syntax

```text
usage: kversion [-h] [-r] [-q]

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
  -q, --quiet   enable quiet mode.
```

# 06-d. Qemu-system/KGDB Cooperation - Virt/Phys/Page
## highmem-dump

Dump HighMem mappings.


### Syntax

```text
usage: highmem-dump [-h] [-s | -S] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -s, --sort-by-virt  sort by virtual address.
  -S, --sort-by-page  sort by page address.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

## p2v

Translate from physical address to virtual address.


### Syntax

```text
usage: p2v [-h] [-S | -s] [-v] ADDRESS

positional arguments:
  ADDRESS        the address of data to translate.

options:
  -h, --help     show this help message and exit
  -S             ARMv7: use TTBRn_ELm_S to parse start. ARMv8: heuristic search the memory of qemu-system.
  -s             ARMv7/v8: use TTBRn_ELm to parse start.
  -v, --verbose  verbose output (for arm64 secure memory).
```

### Examples

```gdb
p2v 0x55041e0
```

## page

The base command to convert between virtual addresses, physical addresses, and page addresses.


### Syntax

```text
usage: page [-h] [-hh] {to_virt,to_phys,from_virt,from_phys} ...

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.

command:
  {to_virt,to_phys,from_virt,from_phys}
```

### Notes

```text
Simplified page structure:

[x86_64 / CONFIG_SPARSEMEM_VMEMMAP]
VMEMMAP_START--------->+-struct page[]-+
                       | pfn#0 page    | --> physmem 0x0
                       +---------------+
                       | pfn#1 page    | --> physmem 0x1000
                       +---------------+
                       | ...           |
                       +---------------+
                       | pfn#N page    | --> ...
                       +---------------+


[arm64 / CONFIG_SPARSEMEM_VMEMMAP]
* This pattern uses `VMEMMAP_START`, but it needs `memstart_pfn` adjustment.
vmemmap--------------->+-struct page[]-----------+
                       | pfn#0 page              | --> physmem 0x0
                       +-------------------------+
                       | ...                     | --> ...
VMEMMAP_START--------->+-------------------------+
                       | pfn#memstart_pfn   page | --> physmem memstart_addr
                       +-------------------------+
                       | pfn#memstart_pfn+1 page | --> physmem memstart_addr+0x1000
                       +-------------------------+
                       | ...                     |
                       +-------------------------+
                       | pfn#memstart_pfn+N page | --> ...
                       +-------------------------+


[x86_32 / CONFIG_FLATMEM]
mem_map--------------->+-struct page[]-+
                       | pfn#0 page    | --> physmem 0x0
                       +---------------+
                       | pfn#1 page    | --> physmem 0x1000
                       +---------------+
                       | ...           |
                       +---------------+
                       | pfn#N page    | --> ...
                       +---------------+


[arm32 / CONFIG_FLATMEM]
* `mem_map` starts at pfn#PHYS_PFN_OFFSET, not pfn#0.
mem_map--------------->+-struct page[]--------------+
                       | pfn#PHYS_PFN_OFFSET   page | --> physmem PHYS_OFFSET
                       +----------------------------+
                       | pfn#PHYS_PFN_OFFSET+1 page | --> physmem PHYS_OFFSET+0x1000
                       +----------------------------+
                       | ...                        |
                       +----------------------------+
                       | pfn#PHYS_PFN_OFFSET+N page | --> ...
                       +----------------------------+


[x86_32 or arm32 / CONFIG_SPARSEMEM]
* This pattern uses `mem_section[]`, i.e. multiple section-specific mem_maps.
* `section_id` can be obtained from `page->flags`.
* `section_mem_map` is encoded and used to locate the page descriptor array.
+-------------------------------------------------------------------------------------------+
|                                                                                           |
|  +-struct mem_section[]-+                                                                 |
|  | section_mem_map      |     +-->+-struct page[]----------------+                        |
|  +----------------------+     |   | pfn#section_start_pfn   page | --> physmem ...        |
+->| section_mem_map      |-----+   |  flags                       | --> section_id (=idx)--+
   +----------------------+         +------------------------------+
   | ...                  |         | pfn#section_start_pfn+1 page | --> physmem ...
   +----------------------+         |  flags                       |
   | section_mem_map      |         +------------------------------+
   +----------------------+         | ...                          |
                                    +------------------------------+
                                    | pfn#section_start_pfn+N page | --> ...
                                    |  flags                       |
                                    +------------------------------+

* CONFIG_SPARSEMEM_EXTREME is currently unsupported by this command.
```

## page from_phys

Resolve the struct page for a physical address.

- Alias: `phys2page`

### Syntax

```text
usage: page from_phys [-h] [-r] ADDRESS

positional arguments:
  ADDRESS       the physical address to translate.

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
```

## page from_virt

Resolve the struct page for a virtual address.

- Alias: `virt2page`

### Syntax

```text
usage: page from_virt [-h] [-r] ADDRESS

positional arguments:
  ADDRESS       the virtual address to translate.

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
```

## page to_phys

Resolve the physical address for a struct page.

- Alias: `page2phys`

### Syntax

```text
usage: page to_phys [-h] [-r] ADDRESS

positional arguments:
  ADDRESS       the page address to translate.

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
```

## page to_virt

Resolve virtual addresses mapped to the page.

- Alias: `page2virt`

### Syntax

```text
usage: page to_virt [-h] [-r] ADDRESS

positional arguments:
  ADDRESS       the page address to translate.

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
```

### Notes

```text
One page may correspond to multiple virtual addresses.
```

## pageinfo

Dump struct page flags and page_type.


### Syntax

```text
usage: pageinfo [-h] (-p PAGE | VIRT)

positional arguments:
  VIRT             virtual address to dump.

options:
  -h, --help       show this help message and exit
  -p, --page PAGE  page address to dump.
```

## slab-virtual

Convert between slab-virtual addresses and page addresses.


### Syntax

```text
usage: slab-virtual [-h] [-r] [-q] {to_virt,to_page,from_virt,from_page} ADDRESS

positional arguments:
  {to_virt,to_page,from_virt,from_page}
                        conversion mode.
  ADDRESS               the address to convert.

options:
  -h, --help            show this help message and exit
  -r, --rescan          do not use cache.
  -q, --quiet           quiet execution.
```

### Notes

```text
This command works only in CONFIG_SLAB_VIRTUAL=y (implemented at https://github.com/thejh/linux).
Used in the Google Kernel CTF mitigation instance.

CONFIG_SLAB_VIRTUAL=n (normal kernel):
  Both `struct slab` and `struct page` directly manage physmap area.

  [physmap area]
                     +------------+
                     | virt       | <-- size: 0x1000
                     +------------+
                     | ...        |
                     +------------+
  [vmemmap area]
                     +------------+
                     | page/slab  | <-- size: sizeof(page) or sizeof(slab)
                     +------------+
                     | ...        |
                     +------------+

CONFIG_SLAB_VIRTUAL=y (mitigated kernel):
  `struct slab` no longer manages physmap area. Instead, `struct slab` manages the slab_data area.

  [physmap area]
                     +------------+
                     | virt       | <-- size: 0x1000
                     +------------+
                     | ...        |
                     +------------+
  [vmemmap area]
                     +------------+
                     | page       | <-- size: sizeof(page)
                     +------------+
                     | ...        |
                     +------------+
  [slab_meta area]
           ^         +------------+ SLAB_BASE_ADDR (=0xfffffe8000000000)
           |         | slab       |
           |         +------------+
    SLAB_META_SIZE   | slab       | <-- meta entry size: STRUCT_SLAB_SIZE               # v6.1~v6.1.55
           |         +------------+                      or sizeof(struct slab)         # v6.1.56~v6.6, v6.12~
           |         | ...        |                      or sizeof(struct virtual_slab) # v6.6~v6.12
           v         +------------+ 
  [slab_data area]
                     +------------+ SLAB_DATA_BASE_ADDR (=0xfffffe8800000000)
                     | virt       | 
                     +------------+
                     | virt       | <-- size: 0x1000
                     +------------+
                     | ...        |
                     +------------+ SLAB_END_ADDR (=0xffffff0000000000)
```

## v2p

Translate from virtual address to physical address.


### Syntax

```text
usage: v2p [-h] [-S | -s] ADDRESS

positional arguments:
  ADDRESS     the address of data to translate.

options:
  -h, --help  show this help message and exit
  -S          ARMv7: use TTBRn_ELm_S to parse start. ARMv8: heuristic search the memory of qemu-system.
  -s          ARMv7/v8: use TTBRn_ELm to parse start.
```

### Examples

```gdb
v2p 0xffffffff855041e0
```

## xp

Dump physical memory taking into account ROM mapping.


### Syntax

```text
usage: xp [-h] /FMT ADDRESS

positional arguments:
  /FMT        specified output format.
  ADDRESS     dump target address.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
xp /16xg 0x11223344
```

# 06-e. Qemu-system/KGDB Cooperation - Linux Symbol/Type
## kload

Load the vmlinux without a load address.


### Syntax

```text
usage: kload [-h] VMLINUX_PATH

positional arguments:
  VMLINUX_PATH  path of the vmlinux.

options:
  -h, --help    show this help message and exit
```

## kmod-load

Load the kernel module without a load address.


### Syntax

```text
usage: kmod-load [-h] [-n] [-q] name path

positional arguments:
  name            name of the loaded module to search for by `kmod`.
  path            path to compiled kernel module.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -q, --quiet     enable quiet mode.
```

### Examples

```gdb
kmod-load sample /path/to/sample.ko
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.
It is useful if you have a kernel module with debuginfo at hand.
```

## ksymaddr-remote

Resolve kernel symbols from kallsyms table.

- Alias: `ks`

### Syntax

```text
usage: ksymaddr-remote [-h] [-t TYPE] [-e] [-r] [-s] [--vmlinux-file VMLINUX_FILE] [-I] [--print-saved-config] [-n] [-v] [-q] [KEYWORD ...]

positional arguments:
  KEYWORD               filter by specific symbol name.

options:
  -h, --help            show this help message and exit
  -t, --type TYPE       filter by symbol type.
  -e, --exact           use exact match.
  -r, --rescan          do not use cache.
  -s, --smart           filter __pfx_*, __ksymtab_*, etc.
  --vmlinux-file VMLINUX_FILE
                        force use your vmlinux file which includes symbols.
  -I, --ignore-loaded-vmlinux
                        force skip parsing loaded vmlinux.
  --print-saved-config  print saved (cached) config contents.
  -n, --no-pager        do not use the pager.
  -v, --verbose         enable verbose mode.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
ksymaddr-remote commit_creds prepare_kernel_cred  # OR search
```

### Notes

```text
GEF caches offset information for parsing kallsyms to speed up this command.
Each cache is used based on kernel version strings.
In other words, in cases where the kernel version is exactly the same and
the CONFIG is slightly different, the offset will be applied incorrectly.
In this case, rescan with `ks -rv` or clear the cache with `gef reset-cache --hard`.
```

## ksymaddr-remote-apply

Apply symbol from kallsyms in memory.

- Alias: `ks-apply`

### Syntax

```text
usage: ksymaddr-remote-apply [-h] [-r] [-q]

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
  -q, --quiet   enable quiet mode.
```

## ktypes

Display kernel type information from /sys/kernel/btf/vmlinux.


### Syntax

```text
usage: ktypes [-h] [-r] [-n]

options:
  -h, --help      show this help message and exit
  -r, --rescan    do not use cache.
  -n, --no-pager  do not use the pager.
```

### Notes

```text
This command requires CONFIG_DEBUG_INFO_BTF=y.
CONFIG_KALLSYMS_ALL=y is not required.
```

## ktypes-load

Load kernel type information from /sys/kernel/btf/vmlinux.

- Alias: `kt-load`

### Syntax

```text
usage: ktypes-load [-h] [-r]

options:
  -h, --help    show this help message and exit
  -r, --rescan  do not use cache.
```

### Notes

```text
This command requires CONFIG_DEBUG_INFO_BTF=y.
CONFIG_KALLSYMS_ALL=y is not required.
```

## vmlinux-to-elf-apply

Apply symbol from kallsyms in memory using vmlinux-to-elf.


### Syntax

```text
usage: vmlinux-to-elf-apply [-h] [-r]

options:
  -h, --help    show this help message and exit
  -r, --rescan  force applying again. (default: reuse vmlinux-to-elf-dump-memory.elf if exists)
```

# 06-f. Qemu-system/KGDB Cooperation - Linux Task
## kfiles

Display open files for each process (shortcut for `ktask -quF`).


### Syntax

```text
usage: kfiles [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## knamespaces

Display namespaces for each process (shortcut for `ktask -quN`).


### Syntax

```text
usage: knamespaces [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## kregs

Display saved registers for each process (shortcut for `ktask -qur`).


### Syntax

```text
usage: kregs [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## ksighands

Display signal handlers for each process (shortcut for `ktask -qus`).


### Syntax

```text
usage: ksighands [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## ktask

Display process list.


### Syntax

```text
usage: ktask [-h] [-hh] [-f FILTER] [-T TASK_FILTER] [-m] [-r] [-i] [-t] [-F] [-s] [-S] [-N] [-u] [--init-task INIT_TASK] [--meta] [--all] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -f, --filter FILTER   comm string REGEXP filter.
  -T, --task-filter TASK_FILTER
                        task address filter.
  -m, --print-maps      print memory map for each user-land process.
  -r, --print-regs      print general registers saved on kstack for each user-land process.
  -i, --print-all-id    print suid, sgid, euid, egid, fsuid and fsgid.
  -t, --print-thread    display by thread (LWP), not by process.
  -F, --print-fd        print file descriptors for each user process.
  -s, --print-sighand   print signal handlers for each user process.
  -S, --print-seccomp   dump the seccomp filter. If the tool is available, it dumps orig_prog; otherwise, it disassembles bpf_func.
  -N, --print-namespace
                        print namespaces for each user process.
  -u, --user-process-only
                        display user-land process (+ thread) only.
  --init-task INIT_TASK
                        specifies the address of init_task.
  --meta                display offset information.
  --all                 enable all option.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
ktask -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified task_struct structure:

    +-init_task-+
    | list_head |---+    +-->+-kstack----------+    +--->+-vm_area_struct--+
    +-----------+   |    |   | (thread_info)   |    |    | vm_start        |
                    |    |   | STACK_END_MAGIC |    |    | vm_end          |
+-------------------+    |   | ...             |    |    | vm_next (~6.1)  |
|                        |   | ...             |    |    | ...             |
|   +-task_struct---+    |   | ...             |    |    | vm_flags        |
|   | (thread_info) |    |   | ...             |    |    | vm_file         |-----+
|   | ...           |    |   | pt_regs         |    |    | ...             |     |
|   | stack         |----+   +-----------------+    |    +-----------------+     |
|   | ...           |                               |                            |
+-->| tasks         |-->...               +---------+<------------------------+  |
    | ...           |                     |                                   |  |
    | mm            |-->+-mm_struct----+  |  +-------->+-maple_node(6.1~)--+  |  |
    | ...           |   | mmap (~6.1)  |--+  |         | ...               |  |  |
    | pid           |   | ...          |     |         | mr64|ma64|alloc   |  |  |
    | tid           |   | mm_mt (6.1~) |     |         |   ...             |  |  |
    | ...           |   |   ma_root    |-----+         |   slot[]          |--+  |
    | stack_canary  |   | ...          |               +-------------------+     |
    | ...           |   +--------------+                                         |
    | group_leader  |                                         +------------------+       +-mount----------+
    | ...           |         +-->+-cred--------------+       |                          | ...            |
    | thread_group  |-->...   |   | ...               |       |                          | mnt_parent     |-->mount
    | ...           |         |   | uid, gid          |       |                          | mnt_mountpoint |-->dentry
    | cred          |---------+   | suid, sgid        |       |                       +->| mnt (vfsmount) |
    | ...           |             | euid, egid        |       |                       |  |   mnt_root     |-->dentry
    | comm[16]      |             | fsuid, fsgid      |       |                       |  |   ...          |
    | ...           |             | ..., user_ns, ... |       |                       |  | ...            |
    | files         |--+          +-------------------+       |                       |  +----------------+
    | ...           |  |                                      |                       |
    | nsproxy       |------->+-nsproxy----------------+       |                       | +--->+-dentry-----+
    | ...           |  |     | count                  |       |                       | |    | ...        |
    | sighand       |-----+  | uts_ns, ipc_ns, mnt_ns |       |                       | |    | d_parent   |-->dentry
    | ...           |  |  |  | pid_ns_for_children    |       |                       | |    | ...        |
    | seccomp       |  |  |  | net_ns, time_ns, ...   |       |                       | |    | d_inode    |--+
    | ...           |  |  |  +------------------------+       |                       | |    | d_iname    |  |
    +---------------+  |  |                                   |                       | |    | ...        |  |
                       |  +->+-sighand_struct----+            |                       | |    +------------+  |
                       |     | ...               |            v                       | |                    |
                       |     | action[64]        |            +-->+-file-----------+  | | +------------------+
+----------------------+     +-------------------+            |   | ...            |  | | |
|                                                             |   | f_path         |  | | v
+-->+-files_struct-+  +-->+-fdtable---+  +-->+-file*[]-----+  |   |   mnt          |--+ | +->+-inode------+
    | ...          |  |   | max_fds   |  |   | [0]         |--+   |   dentry       |----+ |  | ...        |
    | fdt          |--+   | fd        |--+   | ...         |      | f_inode (3.9~) |------+  | i_ino      |
    | ...          |      | ...       |      | [max_fds-1] |      | ...            |         | ...        |
    +--------------+      +-----------+      +-------------+      +----------------+         +------------+

This command will only track tasks that can be tracked from `init_task` or the result of `kcurrent` command.
Other tasks (such as `swapper/1` if thread 1 is running some task) will not be detected.
```

# 06-g. Qemu-system/KGDB Cooperation - Linux Advanced
## kbdev

Display block device list.


### Syntax

```text
usage: kbdev [-h] [-n] [-q]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -q, --quiet     enable quiet mode.
```

### Examples

```gdb
kbdev -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.
If there are too many block devices, detection may fail.
This is because block devices are not managed in a single location,
so the list of bdev_cache obtained from the slub-dump results is used.
```

## kbpf

Dump the BPF information.


### Syntax

```text
usage: kbpf [-h] [-hh] [-p] [-m] [-n] [-v] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -p, --only-progs    print progs only.
  -m, --only-maps     print maps only.
  -n, --no-pager      do not use the pager.
  -v, --verbose       enable verbose mode.
  -q, --quiet         show result only.
```

### Examples

```gdb
kbpf -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified bpf structure:

+-prog_idr----+   +--->+-xa_node----------+   +--------->+-bpf_prog-------------+
| idr_rt      |   |    | shift            |   |          | ...                  |
|   xa_lock   |   |    | ...              |   |          | type                 |
|   xa_flags  |   |    | count            |   |          | expected_attach_type |
|   xa_head   |---+    | ...              |   |          | len                  |
| idr_base    |        | slots[0]         |---+          | jited_len            |
| idr_next    |        | slots[1]         |--->xa_node   | tag[8]               |
+-------------+        | ...              |    or        | ...                  |
                       | slots[15 or 63]  |    bpf_prog  | bpf_func             |---> BPF-code
                       | ...              |              | ...                  |
                       +------------------+              | aux                  |
                                                         | ...                  |
                                                         +----------------------+

+-map_idr-----+   +--->+-xa_node----------+   +--------->+-bpf_array------------+
| idr_rt      |   |    | shift            |   |          | map                  |
|   xa_lock   |   |    | ...              |   |          |   ...                |
|   xa_flags  |   |    | count            |   |          |   map_type           |
|   xa_head   |---+    | ...              |   |          |   key_size           |
| idr_base    |        | slots[0]         |---+          |   value_size         |
| idr_next    |        | slots[1]         |--->xa_node   |   max_entries        |
+-------------+        | ...              |    or        |   ...                |
                       | slots[15 or 63]  |    bpf_array | elem_size            |
                       | ...              |              | index_mask           |
                       +------------------+              | ...                  |
                                                         +----------------------+
                                                         | value[0]             |
                                                         | value[1]             |
                                                         | ...                  |
                                                         | value[max_entries-1] |
                                                         +----------------------+
```

## kcdev

Display character device list.


### Syntax

```text
usage: kcdev [-h] [-hh] [-n] [-v] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -v, --verbose       enable verbose mode.
  -q, --quiet         enable quiet mode.
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified cdev structure:

+-chrdevs[255]-+    +-char_device_struct-+
| [0]          |--->| next               |--->...
| ...          |    | major              |
| [254]        |    | baseminor          |           +--->+-cdev--+  +-->+-kobject-+
+--------------+    | minorct            |           |    | kobj  |--+   | name    |
                    | name[64]           |           |    | ...   |      | ...     |
                    | cdev               |-----------+    | ops   |      | parent  |
                    +--------------------+           |    | ...   |      | ...     |
                                                     |    | dev   |      +---------+
+----------+    +-kobj_map----+    +-probe-+         |    | ...   |
| cdev_map |--->| probes[0]   |--->| next  |--->...  |    +-------+
+----------+    | ...         |    | dev   |         |
                | probes[254] |    | ...   |         |
                | lock        |    | data  |---------+
                +-------------+    +-------+

The character devices are managed at chrdevs[] and cdev_map.
This command use each of them for getting structure information.
```

## kclock-source

Dump the clocksource list.


### Syntax

```text
usage: kclock-source [-h] [-hh] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -q, --quiet         enable quiet mode.
```

### Notes

```text
Simplified clocksource structure:

                        +-clocksource-+
                        | read        |
+-clocksource_list-+    | ...         |
| list_head        |--->| list        |--->...
+------------------+    | ...         |
                        +-------------+
```

## kconfig

Dump the kernel config if available.


### Syntax

```text
usage: kconfig [-h] [-f FILTER] [-r] [-n] [-q]

options:
  -h, --help           show this help message and exit
  -f, --filter FILTER  REGEXP include filter.
  -r, --rescan         do not use cache.
  -n, --no-pager       do not use the pager.
  -q, --quiet          enable quiet mode.
```

## kdevio

Dump I/O-port and I/O-memory information.


### Syntax

```text
usage: kdevio [-h] [-hh] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

### Notes

```text
Simplified ioport structure:

+-ioport_resource-+       +-------->+-resource--------+
| start           |       |         | start           |
| end             |       |         | end             |
| name            |       |         | name            |
| flags           |       |         | flags           |
| desc            |       |         | desc            |
| parent          |-------+         | parent          |
| sibling         |--> resource     | sibling         |
| child           |--> resource     | child           |
+-----------------+                 +-----------------+

Simplified iomem structure:

+-iomem_resource--+       +-------->+-resource--------+
| start           |       |         | start           |
| end             |       |         | end             |
| name            |       |         | name            |
| flags           |       |         | flags           |
| desc            |       |         | desc            |
| parent          |-------+         | parent          |
| sibling         |--> resource     | sibling         |
| child           |--> resource     | child           |
+-----------------+                 +-----------------+
```

## kdmabuf

Dump DMA-BUF information.


### Syntax

```text
usage: kdmabuf [-h] [-hh] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

### Notes

```text
Simplified DMA-BUF structure:

                     +-dma_buf-----+      +-dma_buf-----+
                     | size        |      | size        |
                     | file        |      | file        |
                     | ...         |      | ...         |
                     | exp_name    |      | exp_name    |
                     | name        |      | name        |
+---------+          | ...         |      | ...         |
| db_list |--------->| list_node   |----->| list_node   |-->...
+---------+          | priv        |--+   | priv        |
 v6.10+:debugfs_list | ...         |  |   | ...         |
 v6.16+:dmabuf_list  +-------------+  |   +-------------+
                                      |
     +--------------------------------+
     |
     +--->+-system_heap_buffer-+  +-->+-scatterlist--+
          | ...                |  |   | page_link    |----->+------+
          | len                |  |   | offset       |      | page |
          | sg_table           |  |   | length       |      +------+
          |   sgl              |--+   | ...          |
          |   ...              |      +--------------+
          | ...                |      | page_link    |-->page
          +--------------------+      | offset       |   or
                                      | length       |   scatterlist
                                      | ...          |
                                      +--------------+
                                      | ...          |
                                      +--------------+
```

## kdmesg

Dump the ring buffer of the dmesg area.


### Syntax

```text
usage: kdmesg [-h] [-hh] [-c] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -c, --use-cache     use previous result.
  -n, --no-pager      do not use the pager.
  -q, --quiet         enable quiet mode.
```

### Examples

```gdb
kdmesg -q
```

### Notes

```text
The information such as [T1] is the thread ID.
Originally, this information is displayed when CONFIG_PRINTK_CALLER=y.
However it is always displayed because it is useful.

Simplified dmesg structure (5.10~):

+-----+
| prb |--+
+-----+  |
         |
+--------+
|
+->+-printk_rb_static-+  +-------------------------->+-prb_desc[]----+
   | desc_ring        |  |                       +---| state_var     |---+
   |   count_bits     |  | +->+-printk_info[]-+  |   | ...           |   |
   |   descs          |--+ |  | seq           |  |   +---------------+   |
   |   infos          |----+  | ts_nsec       |  |   | state_var     |   |
   |   head_id        |       | text_len      |  |   | ...           |   |
   |   tail_id        |       | facility      |  |   +---------------+   |
   |   ...            |       | flags, level  |  |   | ...           |   |
   | text_data_ring   |       | caller_id     |  |   +---------------+<--+
   |   size_bits      |       | dev_info      |  |   | state_var     |
   |   data           |--+    +---------------+  |   | text_blk_lpos |
   |   head_lpos      |  |    | seq           |  |   |   begin       |(=text block start offset)
   |   tail_lpos      |  |    | ts_nsec       |  |   |   next        |(=text block end offset)
   | fail             |  |    | text_len      |  |   +---------------+
   +------------------+  |    | facility      |  |   | state_var     |
                         |    | flags, level  |  |   | text_blk_lpos |
+------------------------+    | caller_id     |  |   |   begin       |
|                             | dev_info      |  |   |   next        |
+->+-printk_record-+          +---------------+  |   +---------------+
   | info          |          | ...           |  |
   | text_buf      |-->text   +---------------+<-+
   | text_buf_size |          | seq           |
   +---------------+          | ...           |
                              +---------------+
* prb_desc and printk_info are accessed in two ways. One is seq number based access which is simply incremented
  and the other is id number based access by lower bit of state_var.
  1-A. (Seq-based prb_desc): Preserving entry state and entry index (=id).
  1-B. (Id-based prb_desc): Preserving begin and next.
  2-A. (Seq-based printk_info): Preserving text data length, time, thread ID, etc. for each entry.
  2-B. (Id-based printk_info): Preserving seq for ring buffer reuse.

Simplified dmesg structure (~5.10):

+-----------+
| __log_buf |-------->+-log_buffer-----+   ^     ^
+-----------+         | ts_nsec        |   |     |
                      | len            |-->|     |
                      | text_len       |   |     |
                      | ...            |   |     |
                      | text[text_len] |   |     |
                      +----------------+   v     |
+---------------+     | ...            |         |
| log_first_idx |---->+----------------+         |
+---------------+     | ts_nsec        |         |
 =start               | len            |         |    +-------------+
                      | text_len       |         |<---| log_buf_len |
                      | ...            |         |    +-------------+
                      | text[text_len] |         |
                      +----------------+         |
+---------------+     | ...            |         |
| log_next_idx  |---->+----------------+         |
+---------------+     | ts_nsec        |         |
 =end                 | len            |         |
                      | text_len       |         |
                      | ...            |         |
                      | text[text_len] |         |
                      +----------------+         v
```

## kfilesystems

Dump filesystems.

- Alias: `kmounts`

### Syntax

```text
usage: kfilesystems [-h] [-hh] [-s] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -s, --skip-mount-path
                        skip resolving path.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified file_systems structure:

                  +-->+-file_system_type-+  +-->+-file_system_type-+  +-->...
                  |   | name             |  |   | name             |  |
+--------------+  |   | ...              |  |   | ...              |  |
| file_systems |--+   | next             |--+   | next             |--+
+--------------+      | fs_supers        |--+   | fs_supers        |
                      | ...              |  |   | ...              |
                      +------------------+  |   +------------------+
                                            |
   +----------------------------------------+
   |
   |   +-super_block-+   +-super_block-+             +-mount--------+
   |   | s_list      |   | s_list      |             | ...          |
   |   | ...         |   | ...         |             | mnt          |
   |   | s_mounts    |   | s_mounts    |---------+   |   mnt_root   |
   |   | ...         |   | ...         |         |   |   ...        |
   +-->| s_instances |-->| s_instances |-->...   |   | ...          |
       | ...         |   | ...         |         +-->| mnt_instance |
       +-------------+   +-------------+             | ...          |
                                                     +--------------+
```

## kipcs

Dump IPCs information (System V semaphore, message queue and shared memory).


### Syntax

```text
usage: kipcs [-h] [-hh] [-v] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -v, --verbose       dump the beginning of msg_msg.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified ipc structure:

+-task_struct-+  +-->+-nsproxy--+  +-->+-ipc_namespace-+
| ...         |  |   | ...      |  |   | ...           |
| nsproxy     |--+   | ipc_ns   |--+   | ids[0] (sem)  |
| ...         |      | ...      |      |   ...         |
+-------------+      +----------+      |   ipcs_idr    |
                                       |     xa_head   |-->xarray-->+-sem_array-+
                                       |     ...       |            | ...       |
                                       | ids[1] (msg)  |            +-----------+
                                       |   ...         |
                                       |   ipcs_idr    |
                                       |     xa_head   |-->xarray-->+-msg_queue-+
                                       |     ...       |            | ...       |
                                       | ids[2] (shm)  |            +-----------+
                                       |   ...         |
                                       |   ipcs_idr    |
                                       |     xa_head   |-->xarray-->+-shmid_kernel-+
                                       |     ...       |            | ...          |
                                       | ...           |            +--------------+
                                       +---------------+
```

## kirq

Dump IRQ (interrupt request) information.


### Syntax

```text
usage: kirq [-h] [-hh] [-n] [-v] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -v, --verbose       enable verbose mode.
  -q, --quiet         show result only.
```

### Notes

```text
Simplified irq structure:

+-irq_desc_tree(~6.5)-+   +--->+-xa_node---------+   +--->+-irq_desc----+
| xa_lock             |   |    | shift           |   |    | ...         |
| xa_flags            |   |    | ...             |   |    | irq_data    |
| xa_head             |---+    | count           |   |    |   ...       |
+---------------------+        | ...             |   |    |   irq       |
                               | slots[0]        |---+    |   ...       |
                               | slots[1]        |   ^    | ...         |
                               | ...             |   |    | action      |
                               | slots[15 or 63] |   |    |   handler   |
                               | ...             |   |    |   ...       |
                               +-----------------+   |    |   name      |
                                                     |    |   ...       |
+-sparce_irq(6.5~)-+   +-->+-maple_node------+       |    | ...         |
| ...              |   |   | ...             |       |    +-------------+
| ma_root          |---+   | mr64|ma64|alloc |       |
| ...              |       |   ...           |       |
+------------------+       |   slot[]        |-------+
                           +-----------------+
```

## kmod

Display kernel module list.


### Syntax

```text
usage: kmod [-h] [-hh] [-s | -a] [--symbol-unsort] [-f FILTER] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -s, --resolve-symbol  try to resolve symbols.
  -a, --apply-symbol    try to apply symbol in the form 'module_name.symbol'.
  --symbol-unsort       print resolved symbols without sorting by address.
  -f, --filter FILTER   REGEXP filter.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
kmod -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified module structure:

                   +-module------------------+
+-modules-----+    | ...                     |
| list_head   |--->| list                    |--->...
+-------------+    | name[]                  |
                   | ...                     |
                   | mem[] (v6.4~)           |
                   |     base                |
                   |     size                |
                   |     ...                 |
                   | init_layout (v4.5~v6.4) |
                   |     base                |
                   |     size                |
                   |     text_size           |
                   |     ro_size             |
                   |     ro_after_init_size  |
                   |     ...                 |
                   | module_core    (~v4.4)  |
                   | init_size      (~v4.4)  |
                   | core_size      (~v4.4)  |
                   | init_text_size (~v4.4)  |  +-->+-mod_kallsyms---+
                   | core_text_size (~v4.4)  |  |   | symtab         |
                   | ...                     |  |   | num_symtab     |
                   | kallsyms                |--+   | strtab         |
                   | ...                     |      | typetab (v5.2~)|
                   +-------------------------+      +----------------+

Notes for -a option:
- You can check the added symbols with the `symbols` command.
- Added symbols are in the format `module_name.symbol` to avoid collisions.
  When used from the command line, they must be enclosed in single quotes.
  e.g., `p 'virtio_net.__this_module'`
```

## knetdev

Dump net device information.


### Syntax

```text
usage: knetdev [-h] [-hh] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

### Notes

```text
Simplified net_device structure:

                     +-net_device--------+    +-net_device--------+
                     | ... (v6.8~)       |    | ... (v6.8~)       |
+-init_net------+    | name[]            |    | name[]            |
| ...           |    | ...               |    | ...               |
| dev_base_head |--->| dev_list          |--->| dev_list          |--->...
| ...           |    | ...               |    | ...               |
+---------------+    +-------------------+    +-------------------+
```

## kops

Display the members of commonly used function table (like struct file_operations) in the kernel.


### Syntax

```text
usage: kops [-h] [-V VERSION] [-n] [-q] STRUCT_NAME [ADDRESS]

positional arguments:
  STRUCT_NAME           the structure name.
  ADDRESS               the address interpreted as ops.

options:
  -h, --help            show this help message and exit
  -V, --version VERSION
                        use specific kernel version. (default: detected kernel version)
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
kops file_operations
kops -V 6.6.0 file_operations
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Currently it supports from 3.0 to 7,0-rc7.

Supported structure:
  address_space_operations, ata_port_operations, btf_kind_operations, block_device_operations,
  clk_ops, configfs_item_operations, configfs_group_operations, damon_operations,
  dentry_operations, dev_pm_ops, dma_buf_ops, export_operations,
  file_operations, fs_context_operations, inode_operations, kobj_ns_type_operations,
  media_entity_operations, movable_operations, net_device_ops, page_ext_operations,
  parport_operations, pernet_operations, pipe_buf_operations, proc_ns_operations,
  proc_ops, regulator_ops, seq_operations, smp_operations,
  super_operations, tty_ldisc_ops, tty_operations, tty_port_operations,
  ucsi_operations, vm_operations_struct,
```

## kpcidev

Dump the PCI devices.


### Syntax

```text
usage: kpcidev [-h] [-n] [-v] [-q]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   enable verbose mode.
  -q, --quiet     enable quiet mode.
```

### Notes

```text
Simplified pcidev structure:

+----------------+   +-pci_bus--------+
| pci_root_buses |-->| node.next      |-->...
+----------------+   | node.prev      |
                     | parent         |    +-pci_dev----------+
                     | children.next  | +->| bus_list.next    |-->...
                     | children.prev  | |  | bus_list.prev    |
                     | devices.next   |-+  | ...              |
                     | devices.prev   |    | vendor           |
                     | ...            |    | device           |
                     | dev            |    | subsystem_vendor |
                     |   kobj         |    | subsystem_device |
                     |     name       |    | class            |
                     | ...            |    | revision         |
                     +----------------+    | dev              |
                                           |   kobj           |
                                           |     name         |
                                           | ...              |
                                           | +-resource[0]-+  |
                                           | | start       |  |
                                           | | end         |  |
                                           | | name        |  |
                                           | | flags       |  |
                                           | | ...         |  |
                                           | +-resource[1]-+  |
                                           | | ...         |  |
                                           | +-------------+  |
                                           | | ...         |  |
                                           | +-------------+  |
                                           | ...              |
                                           +------------------+
```

## kpipe

Dump pipe information.


### Syntax

```text
usage: kpipe [-h] [-hh] [-i INODE_FILTER] [-f FILE_FILTER] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -i, --inode-filter INODE_FILTER
                        filter by specific struct inode.
  -f, --file-filter FILE_FILTER
                        filter by specific struct file.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

### Examples

```gdb
kpipe -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified pipe structure:

+-task_struct-+  +->+-files_struct-+  +->+-fdtable---+  +->+-files*[]----+  +->+-file------+
| ...         |  |  | ...          |  |  | max_fds   |  |  | [0]         |--+  | ...       |
| files       |--+  | fdt          |--+  | fd        |--+  | ...         |     | f_path    |
| ...         |     | ...          |     | ...       |     | [max_fds-1] |     |   dentry  |---+
+-------------+     +--------------+     +-----------+     +-------------+     | ...       |   |
                                                                               +-----------+   |
                                                                                               |
+----------------------------------------------------------------------------------------------+
|
|  +-dentry---+  +->+-inode-----+  +->+-pipe_inode_info--------+  +->+-pipe_buffer-+
|  | ...      |  |  | ...       |  |  | ...                    |  |  | page        |--->page
+->| d_inode  |--+  | i_pipe    |--+  | head, tail, (v5.5~)    |  |  | offset      |
   | ...      |     | ...       |     | max_usage, (v5.5~)     |  |  | len         |
   +----------+     +-----------+     | ring_size, (v5.5~)     |  |  | ...         |
                                      | nrbuf, curbuf, (~v5.4) |  |  +-------------+
                                      | buffers (~v5.4)        |  |  | page        |--->page
                                      | ...                    |  |  | offset      |
                                      | bufs                   |--+  | len         |
                                      | ...                    |     | ...         |
                                      +------------------------+     +-------------+
                                                                     | ...         |
                                                                     +-------------+
```

## ksysctl

Dump the sysctl parameters.


### Syntax

```text
usage: ksysctl [-h] [-hh] [-f FILTER] [-s] [-e] [-r] [-v] [-n] [-q]

options:
  -h, --help           show this help message and exit
  -hh, --help-simple   show help without ASCII diagram.
  -f, --filter FILTER  REGEXP filter.
  -s, --skip-symlink   do not follow symlink (net.* and user.*).
  -e, --exact          use exact match.
  -r, --rescan         do not use cache.
  -v, --verbose        dump zero-sized entries too.
  -n, --no-pager       do not use the pager.
  -q, --quiet          enable quiet mode.
```

### Examples

```gdb
ksysctl -q
```

### Notes

```text
This command requires CONFIG_RANDSTRUCT=n.

Simplified sysctl_table structure:

   +-sysctl_table_root-+          +----->+-ctl_dir------+
   | default_set       |          |      | header       |
   |   ...             |          |      |   ctl_table  |---+
   |   dir             |          |      |   ...        |   |
   |     header        |          |      |   parent     |---|-->parent ctl_node
   |       ctl_table   |          |      |   ...        |   |
   |       ...         |          |      | root         |   |
   |       parent      |          |      |   rb_node    |---|-->ctl_node
   |       ...         |          |      +--------------+   |
   |     root          |          |                         |
   |       rb_node     |----+     |   +---------------------+
   |   ...             |    |     |   |
   +-------------------+    |     |   +->+-ctl_table(array)-+
                            |     |      | procname         |-->name[]
+---------------------------+     |      | data             |-->data[max_len]
|                                 |      | maxlen           |
+->+-ctl_node-----+               |      | mode             |
   | rb_node      |               |      | proc_handler     |
   |   color      |               |      +------------------+
   |   right      |--->ctl_node   |      | procname         |-->name[]
   |   left       |--->ctl_node   |      | data             |-->data[max_len]
   | header       |---------------+      | maxlen           |
   +--------------+                      | mode             |
                                         | proc_handler     |
                                         +------------------+
                                         | ...              |
                                         +------------------+
```

## ktimer

Dump the timer.


### Syntax

```text
usage: ktimer [-h] [-hh] [-n] [-q]

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -n, --no-pager      do not use the pager.
  -q, --quiet         enable quiet mode.
```

### Notes

```text
Simplified timer structure (per-cpu):

+-timer_bases[0]----+    +-timer_list--+    +-timer_list--+
| ...               |    | entry       |    | entry       |
| vectors[0]        |--->|   next      |--->|   next      |--->...
| ...               |    |   pprev     |    |   pprev     |
| vectors[512or576] |    | expires     |    | expires     |
| ...               |    | function    |    | function    |
+-timer_bases[1]----+    | ...         |    | ...         |
| ...               |    +-------------+    +-------------+
| vectors[0]        |
| ...               |
| vectors[512or576] |
| ...               |
+-------------------+

Simplified hrtimer structure (per-cpu):

+-hrtimer_cpu_bases-+
| ...               |
| clock_bases[0]    |   +--->+-hrtimer------+
|   ...             |   |    | node         |
|   clockid         |   |    |   node       |
|   ...             |   |    |     color    |
|   active          |   |    |     right    |--->hrtimer
|      rb_root      |   |    |     left     |--->hrtimer
|        rb_root    |---+    |   expires    |
|        ...        |        | ...          |
|   get_time        |        | function     |
|   ...             |        | ...          |
| ...               |        +--------------+
| clock_bases[8]    |
|   ...             |
+-------------------+
```

## syscall-table-view

Display syscall_table entries.

- Alias: `kst`

### Syntax

```text
usage: syscall-table-view [-h] [-f FILTER] [-n] [-q]

options:
  -h, --help           show this help message and exit
  -f, --filter FILTER  REGEXP filter.
  -n, --no-pager       do not use the pager.
  -q, --quiet          enable quiet mode.
```

### Examples

```gdb
syscall-table-view
syscall-table-view --filter write
```

# 06-h. Qemu-system/KGDB Cooperation - Linux Allocator
## buddy-dump

Dump the zone of the page allocator (buddy allocator) free-list.

- Alias: `zone-dump`, `pcplist`

### Syntax

```text
usage: buddy-dump [-h] [-hh] [-z {DMA,DMA32,Normal,HighMem,Movable,Device}] [-o ORDER_FILTER] [-m MTYPE_FILTER] [-p PCP_INDEX_FILTER] [-P] [-F] [--cpu CPU] [-s] [-S] [-Q] [-M] [--MIGRATE_PCPTYPES {3,4}] [-r] [-c N] [-v] [-vv] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -z, --zone {DMA,DMA32,Normal,HighMem,Movable,Device}
                        filter by specified zone name.
  -o, --order ORDER_FILTER
                        filter by specified order.
  -m, --mtype MTYPE_FILTER
                        filter by specified mtype.
  -p, --pcp-index PCP_INDEX_FILTER
                        filter by specified per-cpu index.
  -P, --only-pcp        dump only per-cpu pages.
  -F, --skip-pcp        skip dumping per-cpu pages (dump only free_area).
  --cpu CPU             filter by specific cpu for per-cpu pages.
  -s, --sort            sort by page address instead of link list order of each size. overrides -c to 0.
  -S, --sort-verbose    enable --sort and add used area. filtered areas are treated as used. overrides -c to 0.
  -Q, --skip-phys       skip virt -> phys translation.
  -M, --use-physmap     use physmap for virt -> phys translation to speed up (when KGDB mode, x64/arm64 only).
  --MIGRATE_PCPTYPES {3,4}
                        use specify value; linux: 3, android: 4 (2023~).
  -r, --rescan          do not use cache.
  -c, --count N         max entries to read per list (default: 5, 0=unlimited). -s/-S/-v/-vv override this to 0.
  -v, --verbose         show all entries for non-sort mode. equivalent to -c 0.
  -vv, --vverbose       show empty entries too for non-sort mode. overrides -c to 0.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

### Examples

```gdb
buddy-dump -z DMA32
buddy-dump -o 1 -o 2
buddy-dump --only-pcp --pcp-index 0 --cpu 0
buddy-dump --sort-verbose
```

### Notes

```text
Simplified buddy allocator structure:

  +-node_data[MAX_NUMNODES]-+
  | *pglist_data (node 0)   |--+
  | *pglist_data (node 1)   |  |
  | *pglist_data (node 2)   |  |
  | ...                     |  |
  +-------------------------+  |
                               |
    +--------------------------+
    |
    v
  +-pglist_data------------------------------+
  | node_zones[MAX_NR_ZONES]                 |
  |   +-node_zones[0]----------------------+ |   +--->+-per_cpu_pages--------+
  |   |  ...                               | |   |    | ...                  |
  |   |  per_cpu_pageset                   |-----+    | lists[NR_PCP_LISTS]  |    +-page-----+
  |   |  ...                               | |        |   +-lists[0]-------+ |    | flags    |
  |   |  name                              | |        |   | next           |----->| lru.next |->...
  |   |  ...                               | |        |   | prev           | |    | lru.prev |
  |   |  free_area[MAX_ORDER]              | |        |   +-lists[1]-------+ |    | ...      |
  |   |    +-free_area[0]----------------+ | |        |   | ...            | |    +----------+
  |   |    | free_list[MIGRATE_TYPES]    | | |        |   +----------------+ |
  |   |    |   +-free_list[0]----------+ | | |        +----------------------+
  |   |    |   | next                  |---------+
  |   |    |   | prev                  | | | |   |
  |   |    |   +-free_list[1]----------+ | | |   |    +-page-----+    +-page-----+    +-page-----+
  |   |    |   | ...                   | | | |   |    | flags    |    | flags    |    | flags    |
  |   |    |   +-----------------------+ | | |   +--->| lru.next |--->| lru.next |--->| lru.next |->...
  |   |    | nr_free                     | | |        | lru.prev |    | lru.prev |    | lru.prev |
  |   |    +-free_area[1]----------------+ | |        | ...      |    | ...      |    | ...      |
  |   |    | ...                         | | |        +----------+    +----------+    +----------+
  |   |    +-----------------------------+ | |
  |   +-node_zones[1]----------------------+ |
  |   |  ...                               | |
  |   +------------------------------------+ |
  | ...                                      |
  +------------------------------------------+

You can combine this result with information of in-use space. Try using `kvmmap` command.
```

## kmem-cache-alias

Resolve the slab cache (kmem_cache) alias.


### Syntax

```text
usage: kmem-cache-alias [-h] [-s] [-m] [-n] [-q] [names ...]

positional arguments:
  names               filter by specific cache name(s) (substring match).

options:
  -h, --help          show this help message and exit
  -s, --sort-by-size  sort by object size.
  -m, --merged-only   show only merged caches grouped by physical cache.
  -n, --no-pager      do not use the pager.
  -q, --quiet         show result only.
```

### Notes

```text
This command requires CONFIG_SYSFS=y.
```

## slab-contains

Resolve the slab cache (kmem_cache) that an object belongs to (for slab/slub/slub-tiny).

- Alias: `xslab`

### Syntax

```text
usage: slab-contains [-h] [-r] [-v] [-q] ADDRESS

positional arguments:
  ADDRESS        target address.

options:
  -h, --help     show this help message and exit
  -r, --rescan   do not use cache.
  -v, --verbose  enable verbose mode.
  -q, --quiet    show result only.
```

### Notes

```text
Simplified page/slab structure:

+-kmem_cache-+
| cpu_slab   |--->+-kmem_cache_cpu-+
| ...        |    | page/slab      |--+
+------------+    | freelist       |  |
      ^           +----------------+  |   <---virt/page translate--->
      |                               v
      |                         +-page/slab---+               +-0x1000-page-+ <--base (named by GEF)
      +-------------------------|  slab_cache |               | chunk       |
      |                         +-page/slab---+               | ...         |
      +-------------------------|  slab_cache |               +-0x1000-page-+
      |                         +-page/slab---+               | chunk       |
      +-------------------------|  slab_cache |               | chunk       | <--user specified address
                                +-------------+               | ...         |
                                                              +-0x1000-page-+
                                                              | chunk       |
                                                              | ...         |
                                                              +-------------+
* Compound pages and huge pages are not supported.
```

## slab-dump

Dump SLAB free-list reachable from slab_caches.


### Syntax

```text
usage: slab-dump [-h] [-hh] [-l] [-L] [--meta] [--cpu CPU] [-R] [-s] [--skip-partial] [--skip-full] [--skip-free] [--hexdump-used SIZE] [--hexdump-freed SIZE] [--telescope-used SIZE] [--telescope-freed SIZE] [-r] [-n] [-q] [SLAB_CACHE_NAME ...]

positional arguments:
  SLAB_CACHE_NAME       filter by specific slab cache name.

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -l, --list            list all slab cache names.
  -L, --list-no-sort    list all slab cache names without sort.
  --meta                display offset information.
  --cpu CPU             filter by specific cpu.
  -R, --reverse-walk    reverse order walk for slab_caches->list_head.
  -s, --simple          skip displaying layout and freelist.
  --skip-partial        skip displaying slabs_partial.
  --skip-full           skip displaying slabs_full.
  --skip-free           skip displaying slabs_free.
  --hexdump-used SIZE   hexdump `used chunks` if layout is resolved.
  --hexdump-freed SIZE  hexdump `unused (freed) chunks` if layout is resolved.
  --telescope-used SIZE
                        telescope `used chunks` if layout is resolved.
  --telescope-freed SIZE
                        telescope `unused (freed) chunks` if layout is resolved.
  -r, --rescan          do not use cached offset.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
```

### Examples

```gdb
slab-dump kmalloc-256          # dump kmalloc-256 from all cpus
slab-dump kmalloc-256 --cpu 1  # dump kmalloc-256 from cpu 1
slab-dump --list               # list slab cache names
```

### Notes

```text
Simplified SLAB structure:

                         +-kmem_cache--+         +-kmem_cache--+   +-kmem_cache--+
                         | cpu_cache   |---+     | cpu_cache   |   | cpu_cache   |
                         | limit       |   |     | limit       |   | limit       |
                         | size        |   |     | size        |   | size        |
                         | flags       |   |     | flags       |   | flags       |
                         | num         |   |     | num         |   | num         |
                         | gfporder    |   |     | gfporder    |   | gfporder    |
       +-slab_caches-+   | name        |   |     | name        |   | name        |
 ...<->| list_head   |<->| list_head   |<------->| list_head   |<->| list_head   |<-> ...
       +-------------+   | object_size |   |     | object_size |   | object_size |
                         | node[]      |------+  | node[]      |   | node[]      |
                         +-------------+   |  |  +-------------+   +-------------+
    +-__per_cpu_offset-+                   |  |
    | cpu0_offset      |--+----------------+  |
    | cpu1_offset      |  |                   |
    | cpu2_offset      |  |                   v                  +-page/slab-+    +-page/slab-+
    | ...              |  |       +-kmem_cache_node-+      +---->| slab_list |--->| slab_list |-->...
    +------------------+  |       | slabs_partial   |------+     | freelist  |    | freelist  |
                          |       | slabs_full      |----->...   | s_mem     |-+  | s_mem     |-+
      +-------------------+       | slabs_free      |----->...   | active    | |  | active    | |
      |                           +-----------------+            +-----------+ |  +-----------+ |
      v                                                                        |                |
    +-array_cache--------+                                         +-----------+    +-----------+
    | avail              |                                         |                |
    | limit              |                                         v                v
    | entry[]            |                                       +-chunk--+       +-chunk--+
    |   freed_chunk_ptr  |-------------------------------------->|        |       |        |
    |   freed_chunk_ptr  |----------------------------+          +-chunk--+       +-chunk--+
    |   freed_chunk_ptr  |                            |          |        |       |        |
    |   freed_chunk_ptr  |                            |          +-chunk--+       +-chunk--+
    |   freed_chunk_ptr  |                            +--------->|        |       |        |
    |   ...              |                                       +-...----+       +-...----+
    +--------------------+
* `struct page` has been split into `struct page` and `struct slab` since kernel 5.17.
  The structure name used for SLAB has been changed to `struct slab`.
* Chunks in array_cache are marked as in-use, even though they are actually reusable.
* SLAB was removed in kernel 6.8.
```

## slob-dump

Dump SLOB free-list reachable from slab_caches.


### Syntax

```text
usage: slob-dump [-h] [-hh] [-l] [-L] [--meta] [-R] [-s] [--large] [--medium] [--small] [-r] [-v] [-n] [-q] [SLOB_CACHE_NAME ...]

positional arguments:
  SLOB_CACHE_NAME     filter by specific slob cache name (need -v option).

options:
  -h, --help          show this help message and exit
  -hh, --help-simple  show help without ASCII diagram.
  -l, --list          list all slob cache names.
  -L, --list-no-sort  list all slob cache names without sort.
  --meta              display offset information.
  -R, --reverse-walk  reverse order walk for slab_caches->list_head.
  -s, --simple        skip showing freelist.
  --large             display only free_slob_large.
  --medium            display only free_slob_medium.
  --small             display only free_slob_small.
  -r, --rescan        do not use cached offset.
  -v, --verbose       enable verbose mode (print kmem_cache).
  -n, --no-pager      do not use the pager.
  -q, --quiet         enable quiet mode.
```

### Examples

```gdb
slob-dump kmalloc-256  # dump kmalloc-256 kmem_cache and all freelists
slob-dump --list       # list slob cache names
```

### Notes

```text
Simplified SLOB structure:

                         +-kmem_cache--+   +-kmem_cache--+   +-kmem_cache--+
                         | object_size |   | object_size |   | object_size |
                         | size        |   | size        |   | size        |
                         | flags       |   | flags       |   | flags       |
       +-slab_caches-+   | name        |   | name        |   | name        |
 ...<->| list_head   |<->| list_head   |<->| list_head   |<->| list_head   |<-> ...
       +-------------+   +-------------+   +-------------+   +-------------+
* slab_caches is not used when traversing the freelist

   +-free_slob_large--+              +-page/slab-----+           +-page/slab-----+
   | list_head        |<---------+   | freelist      |-----+     | freelist      |
   +-free_slob_medium-+          |   | units (total) |     |     | units (total) |
   | list_head        |-->...    +-->| list_head     |<----|---->| list_head     |<->...
   +-free_slob_small--+              +---------------+     |     +---------------+
   | list_head        |-->...                              |
   +------------------+                      +-------------+
   small : size < 0x100                      |
   medium: 0x100 <= size < 0x400             |   +-chunk-----+   +-chunk-----+
   large : 0x400 <= size < 0x1000            +-->| units     |-->| -offset   |-->...
* size is only judged when first inserted,       | offset    |   +-----------+
  so divided remainder is stay on.               +-----------+   (when units=1, stored negative offset)

* `struct page` has been split into `struct page` and `struct slab` since kernel 5.17.
  The structure name used for SLOB has been changed to `struct slab`.
* SLOB was removed in kernel 6.4.
```

## slub-dump

Dump SLUB free-list reachable from slab_caches.


### Syntax

```text
usage: slub-dump [-h] [-hh] [-hs] [-l] [-L] [--meta] [--cpu CPU] [-R] [-s] [-v] [-vv] [--only-partial | --only-node] [--skip-sheaf] [--hexdump-used SIZE] [--hexdump-freed SIZE] [--telescope-used SIZE] [--telescope-freed SIZE] [--slub-debug-y] [-r] [-n] [-q] [--tlbflush-queue] [--skip-page2virt] [--no-xor]
                 [--no-byte-swap] [--offset-random OFFSET_RANDOM] [--offset-node OFFSET_NODE]
                 [SLUB_CACHE_NAME ...]

positional arguments:
  SLUB_CACHE_NAME       filter by specific slub cache name.

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -hs, --help-for-slab-virtual
                        show ASCII diagram for CONFIG_SLAB_VIRTUAL=y.
  -l, --list            list all slub cache names.
  -L, --list-no-sort    list all slub cache names without sort.
  --meta                display offset information.
  --cpu CPU             filter by specific cpu.
  -R, --reverse-walk    reverse order walk for slab_caches->list_head.
  -s, --simple          skip displaying layout and freelist.
  -v, --verbose, --partial
                        kernel < 7.0: dump partial pages too. kernel >= 7.0: ignored.
  -vv, --vverbose, --node
                        kernel < 7.0: dump partial pages and node pages too. kernel >= 7.0: ignored.
  --only-partial        kernel < 7.0: dump only partial pages. kernel >= 7.0: ignored.
  --only-node           kernel < 7.0: dump only node pages. kernel >= 7.0: ignored.
  --skip-sheaf          skip dumping cpu_sheaves / slab_sheaf path (6.18+).
  --hexdump-used SIZE   hexdump `used chunks` if layout is resolved.
  --hexdump-freed SIZE  hexdump `unused (freed) chunks` if layout is resolved.
  --telescope-used SIZE
                        telescope `used chunks` if layout is resolved.
  --telescope-freed SIZE
                        telescope `unused (freed) chunks` if layout is resolved.
  --slub-debug-y        assumes `CONFIG_SLUB_DEBUG=y` and dumps kmem_cache_node->full slabs.
  -r, --rescan          do not use cached offset.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
  --tlbflush-queue      dump `slub_tlbflush_queue` (x86-64 only && CONFIG_SLAB_VIRTUAL=y).
  --skip-page2virt      [FOR DEVELOPER] used internally in gef, please don't use it.
  --no-xor              [FOR DEVELOPER] skip xor to chunk->next when `kmem_cache.random` is falsely detected.
  --no-byte-swap        [FOR DEVELOPER] skip byteswap to chunk->next when `kmem_cache.random` is falsely detected.
  --offset-random OFFSET_RANDOM
                        [FOR DEVELOPER] user-specified offsetof(kmem_cache, random) when `kmem_cache.random` is falsely detected.
  --offset-node OFFSET_NODE
                        [FOR DEVELOPER] user-specified offsetof(kmem_cache, node) when `kmem_cache.node` is falsely detected.
```

### Examples

```gdb
slub-dump kmalloc-256             # <7.0: active pages; 7.0+: cpu sheaves and node slabs
slub-dump kmalloc-256 --cpu 1     # dump kmalloc-256 from cpu 1
slub-dump kmalloc-256 --partial   # <7.0 only: show active pages and partial pages
slub-dump kmalloc-256 --node      # <7.0 only: show active pages, partial pages and node pages
slub-dump --list                  # list slub cache names
slub-dump -vv --offset-node 0xc8  # user specified offsetof(kmem_cache, node)
```

### Notes

```text
Simplified SLUB structure:

                         +-kmem_cache----------+         +-kmem_cache--+   +-kmem_cache--+
                         | cpu_slab (~6.19)    |---+     | cpu_slab    |   | cpu_slab    |
                         | cpu_sheaves (6.18~) |---|-+   | cpu_sheaves |   | cpu_sheaves |
                         | flags               |   | |   | flags       |   | flags       |
                         | size                |   | |   | size        |   | size        |
                         | object_size         |   | |   | object_size |   | object_size |
                         | offset              |   | |   | offset      |   | offset      |
       +-slab_caches-+   | name                |   | |   | name        |   | name        |
 ...<->| list_head   |<->| list_head           |<------->| list_head   |<->| list_head   |<-> ...
       +-------------+   | random              |   | |   | random      |   | random      |
                         | node[]              |-+ | |   | node[]      |   | node[]      |
                         +---------------------+ | | |   +-------------+   +-------------+
                                                 | | |
                                                 | | |     [sheaf/barn (the fastest path)]
    +--------------------------------------------+ | |                     +-->+-slab_sheaf-+
    |   +------------------------------------------+ |                     |   | barn_list  |
    |   |                               +------------+                     |   | size       |
    |   |     +-__per_cpu_offset-+      |                                  |   | objects[]  |
    |   +-----| cpu0_offset      |------+------->+-slub_percpu_sheaves-+   |   |  ptr       |->chunk
    |   |     | cpu1_offset      |               | main                |---+   |  ptr       |->chunk
    |   |     | cpu2_offset      |               | spare               |-->... |  ...       |
    |   |     | ...              |               +---------------------+       +------------+
    |   |     +------------------+
    |   |                                                  [active page freelist (fast path)]
    |   |                                                    +-chunk---+  +-chunk---+
    |   |                                                    | ^       |  | ^       |
    |   |                                                    | |offset |  | |offset |
    |   |                                                    | v       |  | v       |
    |   |                  +-------------------------------->| next    |->| next    |->NULL
    |   v (~6.19)          |                                 +---------+  +---------+
    |  +-kmem_cache_cpu-+  |
    |  | freelist       |--+                               [active page freelist (slow path)]
    |  | page/slab      |---->+-page/slab(active)--+         +-chunk---+  +-chunk---+
    |  | partial        |--+  | freelist           |----+    | ^       |  | ^       |
    |  +----------------+  |  |                    |    |    | |offset |  | |offset |
    |                      |  +------------------ -+    |    | v       |  | v       |
    |                      |                            +--->| next    |->| next    |->NULL
    |                      |                                 +---------+  +---------+
    |                      |
    |                      |                               [partial page freelist]
    |                      +->+-page/slab(partial)-+         +-chunk---+  +-chunk---+
    |                         | freelist           |----+    | ^       |  | ^       |
    |                         | next               |--+ |    | |offset |  | |offset |
    |                         +--------------------+  | |    | v       |  | v       |
    |                                                 | +--->| next    |->| next    |->NULL
    |                           +---------------------+      +---------+  +---------+
    |                           |
    |                           v                          [partial page freelist]
    |                         +-page/slab(partial)-+         +-chunk---+  +-chunk---+
    |                         | freelist           |----+    | ^       |  | ^       |
    |                         | next               |--+ |    | |offset |  | |offset |
    |                         +--------------------+  | |    | v       |  | v       |
    |                                                 | +--->| next    |->| next    |->NULL
    |                           +---------------------+      +---------+  +---------+
    |                           |
    |                           v
    +--+                       ...
       |                                                    [numa node partial page freelist]
       v                      +-page/slab(numa-node)+         +-chunk---+  +-chunk---+
      +-kmem_cache_node-+     | freelist            |----+    | ^       |  | ^       |
      | partial         |---->| next                |--+ |    | |offset |  | |offset |
      | (full)          |     +---------------------+  | |    | v       |  | v       |
  +---| barn (6.18~)    |                              | +--->| next    |->| next    |->NULL
  |   +-----------------+  +---------------------------+      +---------+  +---------+
  |   | ...             |  |
  |   |                 |  |                                [numa node partial page freelist]
  |   +-----------------+  |  +-page/slab(numa-node)+         +-chunk---+  +-chunk---+
  |                        |  | freelist            |----+    | ^       |  | ^       |
  |                        +->| next                |--+ |    | |offset |  | |offset |
  |                           +---------------------+  | |    | v       |  | v       |
  |                                                    | +--->| next    |->| next    |->NULL
  |                        +---------------------------+      +---------+  +---------+
  |                        |
  +----+                   v
       |                  ...
       v
      +-node_barn-----+         +-slab_sheaf-+    +-slab_sheaf-+
      | sheaves_full  |<------->| barn_list  |<-->| barn_list  |<-->
      | sheaves_empty |<-->...  | ...        |    | ...        |
      +---------------+         +------------+    +------------+

* `struct page` has been split into `struct page` and `struct slab` since kernel 5.17.
  The structure name used for SLUB has been changed to `struct slab`.
* If all chunks in certain page (or slab) are in use, they will not be displayed by this command.
  This is because they cannot be reached by parsing from `slab_caches`.
  So use `slab-contains` (if you know the address) or `kvmmap` (if you want to see all slabs even if it takes time).
* `slab_sheaf`/`barn` introduced in 6.18 is not used by default, but used by setting it when calling `kmem_cache_create`.
  `slab_sheaf.objects[]` is a stack that grows downwards and caches freed addresses.
* `kmem_cache_cpu` is removed from 7.0. active/partial slabs no longer exist.
  In kernel >= 7.0, this command dumps `cpu_sheaves` and node slabs by default.
  The top of the stack is represented by `slab_sheaf.size`.
* `--partial`, `--node`, `--only-partial`, and `--only-node` affect only kernel < 7.0.
* To see the CONFIG_SLAB_VIRTUAL ASCII diagram, execute `slub-dump --help-for-slab-virtual`.
```

## slub-tiny-dump

Dump SLUB-TINY free-list reachable from slab_caches.


### Syntax

```text
usage: slub-tiny-dump [-h] [-hh] [-l] [-L] [--meta] [-R] [-s] [--hexdump-used SIZE] [--hexdump-freed SIZE] [--telescope-used SIZE] [--telescope-freed SIZE] [-r] [-n] [-q] [--skip-page2virt] [SLUB_CACHE_NAME ...]

positional arguments:
  SLUB_CACHE_NAME       filter by specific slub cache name.

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -l, --list            list all slub cache names.
  -L, --list-no-sort    list all slub cache names without sort.
  --meta                display offset information.
  -R, --reverse-walk    reverse order walk for slab_caches->list_head.
  -s, --simple          skip displaying layout and freelist.
  --hexdump-used SIZE   hexdump `used chunks` if layout is resolved.
  --hexdump-freed SIZE  hexdump `unused (freed) chunks` if layout is resolved.
  --telescope-used SIZE
                        telescope `used chunks` if layout is resolved.
  --telescope-freed SIZE
                        telescope `unused (freed) chunks` if layout is resolved.
  -r, --rescan          do not use cached offset.
  -n, --no-pager        do not use the pager.
  -q, --quiet           enable quiet mode.
  --skip-page2virt      [FOR DEVELOPER] used internally in gef, please don't use it.
```

### Examples

```gdb
slub-tiny-dump kmalloc-256  # dump kmalloc-256
slub-tiny-dump --list       # list slub cache names
```

### Notes

```text
Simplified SLUB-TINY structure:

                         +-kmem_cache----------+     +-kmem_cache--+   +-kmem_cache--+
                         | cpu_sheaves (6.18~) |     | cpu_sheaves |   | cpu_sheaves |
                         | flags               |     | flags       |   | flags       |
                         | size                |     | size        |   | size        |
                         | object_size         |     | object_size |   | object_size |
                         | offset              |     | offset      |   | offset      |
       +-slab_caches-+   | name                |     | name        |   | name        |
 ...<->| list_head   |<->| list_head           |<--->| list_head   |<->| list_head   |<-> ...
       +-------------+   | node[]              |--+  | node[]      |   | node[]      |
                         +---------------------+  |  +-------------+   +-------------+
                                                  |
    +---------------------------------------------+
    |                                               [numa node partial page freelist]
    v                     +-slab-----------+          +-chunk---+  +-chunk---+
  +-kmem_cache_node-+     | freelist       |----+     | ^       |  | ^       |
  | partial         |---->| next           |--+ |     | |offset |  | |offset |
  +-----------------+     +----------------+  | |     | v       |  | v       |
  | ...             |                         | +---->| next    |->| next    |->NULL
  +-----------------+  +----------------------+       +---------+  +---------+
                       |
                       |                            [numa node partial page freelist]
                       |  +-slab-----------+          +-chunk---+  +-chunk---+
                       |  | freelist       |----+     | ^       |  | ^       |
                       +->| next           |--+ |     | |offset |  | |offset |
                          +----------------+  | |     | v       |  | v       |
                                              | +---->| next    |->| next    |->NULL
                       +----------------------+       +---------+  +---------+
                       |
                       v
                      ...
* SLUB-TINY was introduced in kernel 6.2.
```

## vmalloc-dump

Dump vmalloc used list and freed list.


### Syntax

```text
usage: vmalloc-dump [-h] [-hh] [--only-used] [--only-freed] [--meta] [--hexdump-used SIZE] [--telescope-used SIZE] [-r] [-n] [-q]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  --only-used           display only used area.
  --only-freed          display only freed area.
  --meta                display offset information.
  --hexdump-used SIZE   hexdump `used chunks` if layout is resolved.
  --telescope-used SIZE
                        telescope `used chunks` if layout is resolved.
  -r, --rescan          do not use cache.
  -n, --no-pager        do not use the pager.
  -q, --quiet           show result only.
```

### Examples

```gdb
vmalloc-dump -q
```

### Notes

```text
Simplified vmalloc structure:
                           +-vmap_area--+
                           | va_start   |
(~v6.8)                    | va_end     |
+---------------------+    | ...        |
| vmap_area_list      |--->| list       |--->...
+---------------------+    | ...        |
                           | vm         |---->+-vm_struct--+
                           | ...        |     | ...        |
                           +------------+     | flags      |
                                              | ...        |
                                              +------------+
                           +-vmap_area--+
                           | va_start   |
(v5.2~)                    | va_end     |
+---------------------+    | ...        |
| free_vmap_area_list |--->| list       |--->...
+---------------------+    | ...        |
                           +------------+
```

# 06-i. Qemu-system/KGDB Cooperation - Linux Dynamic Inspection
## kmalloc-allocated-by

Call predefined system-calls and print kmalloc-N chunks allocated and freed (x64 only).


### Syntax

```text
usage: kmalloc-allocated-by [-h] [-f FILTER] [-N] [-t] [-d] [-v]

options:
  -h, --help           show this help message and exit
  -f, --filter FILTER  filter specified name (e.g., kmalloc-XX)
  -N, --print-null     display free(NULL).
  -t, --backtrace      display backtrace.
  -d, --dump-chunk     dump the first 0x40 bytes of each chunk.
  -v, --verbose        print meta information.
```

### Examples

```gdb
kmalloc-allocated-by       # simple output
kmalloc-allocated-by -dtv  # useful output
```

### Notes

```text
Disable `-enable-kvm` option for qemu-system (#PF may occur).
Disable `-smp N` option for qemu-system (write memory error may occur).
Append `tsc=unstable` option for kernel cmdline.
This command requires CONFIG_RANDSTRUCT=n.
```

## kmalloc-tracer

Collect and display information when kmalloc/kfree.


### Syntax

```text
usage: kmalloc-tracer [-h] [-f FILTER] [-T TASK_NAME] [-N] [-t] [-d] [-p] [-v]

options:
  -h, --help            show this help message and exit
  -f, --filter FILTER   filter specified slab name (e.g., kmalloc-XX)
  -T, --task-name TASK_NAME
                        filter specified task name (e.g., sh)
  -N, --print-null      display free(NULL).
  -t, --backtrace       display backtrace.
  -d, --dump-chunk      dump the first 0x40 bytes of each chunk.
  -p, --enable-page-allocator-trace
                        in addition to kmalloc and kfree, it also monitors __alloc_pages and __free_pages.
  -v, --verbose         print meta information.
```

### Examples

```gdb
kmalloc-tracer       # simple output
kmalloc-tracer -dtv  # useful output
```

### Notes

```text
Disable `-enable-kvm` option for qemu-system (#PF may occur).
Append `tsc=unstable` option for kernel cmdline.
Tracing `kmem_cache_alloc` type is not supported.
This command requires CONFIG_RANDSTRUCT=n.
```

## ktrace

Trace kernel functions and arguments.


### Syntax

```text
usage: ktrace [-h] [--task-name TASK_NAME] [--task-addr TASK_ADDR] [-f FILTER] [-e EXCLUDE] [-c] [-q]

options:
  -h, --help            show this help message and exit
  --task-name TASK_NAME
                        task name (from `ktask`) for filtering.
  --task-addr TASK_ADDR
                        task address for filtering.
  -f, --filter FILTER   function include filter (REGEXP).
  -e, --exclude EXCLUDE
                        function exclude filter (REGEXP).
  -c, --commit          actually perform ktrace.
  -q, --quiet           skip tqdm and displaying function name.
```

### Notes

```text
If you set breakpoints in some commonly called functions, it became too slow to be useful.
Use filtering options to reduce the number of functions targeted by breakpoints as much as possible.
```

## thunk-tracer

Collect and display the thunk addresses that are called automatically (x64/x86 only).


### Syntax

```text
usage: thunk-tracer [-h]

options:
  -h, --help  show this help message and exit
```

## usermodehelper-tracer

Collect and display information that is executed by call_usermodehelper_setup.


### Syntax

```text
usage: usermodehelper-tracer [-h]

options:
  -h, --help  show this help message and exit
```

# 06-j. Qemu-system/KGDB Cooperation - TrustZone
## bsm

Set a breakpoint in virtual memory by specifying the physical memory of the secure world.


### Syntax

```text
usage: bsm [-h] [-v] PHYS_ADDRESS

positional arguments:
  PHYS_ADDRESS   the target physical address to set a breakpoint.

options:
  -h, --help     show this help message and exit
  -v, --verbose  verbose output.
```

### Examples

```gdb
bsm 0xe1008d8
```

## optee-bget-dump

Dump bget allocator of OPTEE-Trusted-App.


### Syntax

```text
usage: optee-bget-dump [-h] [-hh] [-m OFFSET_malloc_ctx] [-n] [-v]

options:
  -h, --help            show this help message and exit
  -hh, --help-simple    show help without ASCII diagram.
  -m, --malloc_ctx OFFSET_malloc_ctx
                        The offset of `malloc_ctx` at OPTEE-TA.
  -n, --no-pager        do not use the pager.
  -v, --verbose         verbose output.
```

### Examples

```gdb
optee-bget-dump 0x2a408
```

### Notes

```text
Simplified heap structure:

+-malloc_ctx-------------------+         +-freed chunk------------+
| bufsize prevfree             |<--+ +-->| bufsize prevfree       |= 0 (if upper chunk is used)  +--> ...
| bufsize bsize                |   | |   | bufsize bsize          |= the size of this chunk      |
| struct bfhead *flink         |-----+   | struct bfhead *flink   |------------------------------+
| struct bfhead *blink         |   +-----| struct bfhead *blink   |
| (bufsize totalloc)           |         |                        |
| (long numget)                |         |                        |
| (long numrel)                |         |                        |
| (long numpblk)               |         +-used chunk-------------+
| (long numpget)               |         | bufsize prevfree       |= the size of upper chunk (if upper chunk is freed)
| (long numprel)               |         | bufsize bsize          |= the size of this chunk (negative number)
| (long numdget)               |         | uchar user_data[bsize] |
| (long numdrel)               |         |                        |
| (func_ptr compfcn)           |         |                        |
| (func_ptr acqfcn)            |         +------------------------+
| (func_ptr relfcn)            |
| (bufsize exp_incr)           |
| (bufsize pool_len)           |
| struct malloc_pool* pool     |
| size_t pool_len              |
| (struct malloc_stats mstats) |
+------------------------------+
```

## optee-break-ta

Set a breakpoint to OPTEE-TA.


### Syntax

```text
usage: optee-break-ta [-h] [-v] (-f TA_FILE | TA_OFFSET)

positional arguments:
  TA_OFFSET             The breakpoint target offset of OPTEE-TA.

options:
  -h, --help            show this help message and exit
  -f, --ta-file TA_FILE
                        parse the TA file (or ELF file) and stop at the entry point.
  -v, --verbose         show memory map if stopped at __thread_enter_user_mode.
```

### Examples

```gdb
optee-break-ta 0x2784
optee-break-ta -f /path/to/deadbeef-dead-dead-dead-deaddeadbeef.ta
```

### Notes

```text
It is not straightforward to set a breakpoint on a Trusted Application (TA) while you are still
in the normal world, because at that moment the TA has not yet been loaded into the secure world.

The TA is loaded only when the TEE OS routine thread_enter_user_mode stops for the second time.
 - At the 1st stop, only ldelf (the user-space loader that actually loads the TA) is executed, so the TA is still absent.
 - At the 2nd stop, ldelf has finished and the TA is finally present in memory.

Now, thread_enter_user_mode calls __thread_enter_user_mode.
This __thread_enter_user_mode in TEE OS is written directly in assembly.
Because of this, it is immune to compiler optimizations. By searching memory for the fixed byte sequence
of this assembly routine, we can reliably locate its offset and set your breakpoint there.
```

## optee-shm-list

List dynamic shared-memory buffers currently registered in OP-TEE (for OP-TEE v4.3.0~).


### Syntax

```text
usage: optee-shm-list [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## optee-smc-service-dump

Dump the OPTEE SMC (EL3) service (specifically, the arm-trusted-firmware implementation).


### Syntax

```text
usage: optee-smc-service-dump [-h] [-n] [-v]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   verbose output.
```

## optee-ta-dump

The base command to dump OPTEE Trusted Application.


### Syntax

```text
usage: optee-ta-dump [-h] {memory,dir} ...

options:
  -h, --help    show this help message and exit

command:
  {memory,dir}
```

## optee-ta-dump dir

Dump the OPTEE-Trusted-App list from host directory.


### Syntax

```text
usage: optee-ta-dump dir [-h] [-n] [-v] HOST_DIR

positional arguments:
  HOST_DIR        The host directory where you extracted the guest's /lib/optee_armtz/.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   verbose output.
```

## optee-ta-dump memory

Dump the OPTEE-Trusted-App list from OPTEE kernel memory.


### Syntax

```text
usage: optee-ta-dump memory [-h] [-o] [-n]

options:
  -h, --help            show this help message and exit
  -o, --for-old-version
                        for OP-TEE OS before v3.12.0.
  -n, --no-pager        do not use the pager.
```

### Notes

```text
Walk the global TEE context list (`tee_ctxes`) and print `struct tee_ta_ctx` currently linked to it.
- A context is added to this list the first time its TA is successfully loaded.
  (that is: after `ldelf` has relocated the ELF and handed the entry point back to the OP-TEE core)
- A TA that has never been loaded will therefore not appear here.
- For normal user TAs the entry is removed automatically when the last session is closed and the context is freed,
  so terminated TAs usually vanish from the list.
- `TA_FLAG_SINGLE_INSTANCE`, `TA_FLAG_INSTANCE_KEEP_ALIVE`, early-TAs and pseudo-TAs stay linked once they
  have been created because the core keeps them resident.
- ref_count shows the number of sessions currently open for that TA (the live open-session reference counter),
  not a cumulative load count.
```

## wsm

Write secure memory via qemu-system memory map.


### Syntax

```text
usage: wsm [-h] (--phys | --off | --virt) [-v] {byte,short,dword,qword,string,hex} VALUE ADDRESS

positional arguments:
  {byte,short,dword,qword,string,hex}
                        the mode that represents the value of the argument.
  VALUE                 write value.
  ADDRESS               write target address.

options:
  -h, --help            show this help message and exit
  --phys                treat ADDRESS as a physical address.
  --off                 treat ADDRESS as an offset of secure memory top.
  --virt                treat ADDRESS as a virtual address.
  -v, --verbose         verbose output.
```

### Examples

```gdb
wsm dword 0x41414141 --phys 0xe11e3d0     # absolute (physical/non-ASLR) address of secure memory
wsm string "AA\\x41\\x41" --off 0x11e3d0  # the offset of secure memory
wsm hex "4141 4141" --off 0x11e3d0        # hex string is supported (invalid character is ignored)
wsm byte 0x41 --virt 0x783ae3d0           # secure memory ASLR is supported
```

## xsm

Dump secure memory via qemu-system memory map.


### Syntax

```text
usage: xsm [-h] (--phys | --off | --virt) [-v] /FMT ADDRESS

positional arguments:
  /FMT           specified output format.
  ADDRESS        dump target address.

options:
  -h, --help     show this help message and exit
  --phys         treat ADDRESS as a physical address.
  --off          treat ADDRESS as an offset of secure memory top.
  --virt         treat ADDRESS as a virtual address.
  -v, --verbose  verbose output.
```

### Examples

```gdb
xsm /16xw --phys 0xe11e3d0   # absolute (physical/non-ASLR) address of secure memory
xsm /16xw --off 0x11e3d0     # the offset from secure memory area
xsm /16xw --virt 0x783ae3d0  # secure memory ASLR is supported
```

# 06-k. Qemu-system/KGDB Cooperation - Other
## ksearch-code-ptr

Search the code pointer in kernel data area.


### Syntax

```text
usage: ksearch-code-ptr [-h] [-d DEPTH] [-r MAX_RANGE] [-n]

options:
  -h, --help            show this help message and exit
  -d, --depth DEPTH     depth of reference. (default: 1)
  -r, --max-range MAX_RANGE
                        allowable offset range for each reference. (default: 0)
  -n, --no-pager        do not use the pager.
```

## qemu-device-info

Dump device information for qemu-escape.


### Syntax

```text
usage: qemu-device-info [-h] [-d DEVICE] [-n]

options:
  -h, --help           show this help message and exit
  -d, --device DEVICE  device name.
  -n, --no-pager       do not use the pager.
```

### Examples

```gdb
qemu-device-info -d cydf-vga  # Specify a device name
qemu-device-info -d cydf      # Specify a characteristic part of the device name
```

### Notes

```text
qemu-system must be running on the local host.
```

## uefi-ovmf-info

Print UEFI OVMF info.


### Syntax

```text
usage: uefi-ovmf-info [-h]

options:
  -h, --help  show this help message and exit
```

# 07-a. Misc - Conversion
## addressify

Convert reverse-order hex values to address.


### Syntax

```text
usage: addressify [-h] VALUE [VALUE ...]

positional arguments:
  VALUE       the string to convert.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
addressify "00 30 e0 f7 ff 7f"
addressify 00 30 e0 f7 ff 7f
```

## convert

The base command to convert values to various.


### Syntax

```text
usage: convert [-h] {memory,value} ...

options:
  -h, --help      show this help message and exit

command:
  {memory,value}
```

## convert memory

Convert memory values to various.


### Syntax

```text
usage: convert memory [-h] [-n] [-v] LOCATION SIZE

positional arguments:
  LOCATION        start address for hash calculation.
  SIZE            the size for hash calculation.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
  -v, --verbose   enable verbose mode.
```

### Examples

```gdb
convert memory $rsp 0x20
```

## convert value

Convert values to various.


### Syntax

```text
usage: convert value [-h] [--hex] [-n] [-v] VALUE

positional arguments:
  VALUE           the value or string to convert.

options:
  -h, --help      show this help message and exit
  --hex           interpret VALUE as hex. invalid character is ignored.
  -n, --no-pager  do not use the pager.
  -v, --verbose   enable verbose mode.
```

### Examples

```gdb
convert value 0xdeadbeef
convert value "\\x41\\x42\\x43\\x44" -v
convert value --hex "41 42 43 44" -v
```

## u2d

Convert type (unsigned long <-> double/float).


### Syntax

```text
usage: u2d [-h] VALUE

positional arguments:
  VALUE       the hex value or double value.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
u2d 0xdeadbeef
u2d 0.12345
u2d 1.2345e-1
```

### Notes

```text
Only ~64bit supported (Unsupported 80bit, 128bit)
```

## unsigned

Convert the negative number to unsigned.


### Syntax

```text
usage: unsigned [-h] VALUE

positional arguments:
  VALUE       the value to convert.

options:
  -h, --help  show this help message and exit
```

### Examples

```gdb
unsigned -- -0xa0
```

# 07-b. Misc - Search
## constgrep

Grep for lines with #define in files under /usr/include.


### Syntax

```text
usage: constgrep [-h] GREP_PATTERN

positional arguments:
  GREP_PATTERN  filter by regex.

options:
  -h, --help    show this help message and exit
```

### Examples

```gdb
constgrep '__NR_*'
```

# 07-c. Misc - Generation
## bytearray

Generate a bytearray to be compared with possible badchars (ported from mona.py).


### Syntax

```text
usage: bytearray [-h] [-b BADCHARS] [-d]

options:
  -h, --help   show this help message and exit
  -b BADCHARS  characters to exclude.
  -d           dump to /tmp/gef/bytearray.{txt,bin}.
```

### Examples

```gdb
bytearray -b 414243 -b 51-53 -b 61..63
```

## pattern

The base command to create or search for a De Bruijn cyclic pattern (used pwntools).


### Syntax

```text
usage: pattern [-h] {create,search} ...

options:
  -h, --help       show this help message and exit

command:
  {create,search}
```

## pattern create

Generate a de Bruijn cyclic pattern.

- Alias: `pattc`

### Syntax

```text
usage: pattern create [-h] [-c CHARSET] [SIZE]

positional arguments:
  SIZE                  the size of pattern. (default: 1024)

options:
  -h, --help            show this help message and exit
  -c, --charset CHARSET
                        the charset of pattern. (default: abc..z)
```

## pattern search

Search for the cyclic de Bruijn pattern generated by the `pattern create`.

- Alias: `patto`

### Syntax

```text
usage: pattern search [-h] [-c CHARSET] PATTERN [SIZE]

positional arguments:
  PATTERN               the pattern to offset search.
  SIZE                  the size of pattern. (default: 0x10000)

options:
  -h, --help            show this help message and exit
  -c, --charset CHARSET
                        the charset of pattern. (default: abc..z)
```

### Examples

```gdb
pattern search $pc
pattern search 0x61616164
pattern search aaab
```

## print-format

Print bytes format in high level languages.

- Alias: `pf`, `gethex`

### Syntax

```text
usage: print-format [-h] [-f {py,c,js,asm,hex,hexn,hexs,hexsn}] [-b {8,16,32,64}] [-l LENGTH | -t TO_ADDR] LOCATION

positional arguments:
  LOCATION              the address of data to dump.

options:
  -h, --help            show this help message and exit
  -f {py,c,js,asm,hex,hexn,hexs,hexsn}
                        the output format. (default: hex)
  -b {8,16,32,64}       the size of bit. (default: 8)
  -l LENGTH             the length of array. (default: 256)
  -t TO_ADDR            specify the end address instead of the length.
```

### Examples

```gdb
print-format -f py -b 8 -l 256 $rsp
```

### Notes

```text
"hexn" means hex with new-line.
"hexs" means hex with separator.
```

# 07-d. Misc - Show Example
## ret2dl-hint

Hint for return-to-dl-resolve.


### Syntax

```text
usage: ret2dl-hint [-h]

options:
  -h, --help  show this help message and exit
```

## srop-hint

Hint for sigreturn oriented programming.


### Syntax

```text
usage: srop-hint [-h] [{x86,x64,arm,aarch64}]

positional arguments:
  {x86,x64,arm,aarch64}
                        the target architecture.

options:
  -h, --help            show this help message and exit
```

# 07-e. Misc - Calculation
## crc32rev

Perform CRC32 reverse calculation limited to ASCII character range.


### Syntax

```text
usage: crc32rev [-h] [-p POLY] [--poly-reflected] [-i INIT_VALUE] [-o XOROUT] [--refin] [--no-refin] [--refout] [--no-refout]
                [--preset {,base,ieee,isohdlc,adccp,v42,xz,pkzip,aixm,q,autosar,base91d,d,bzip2,aal5,dectb,b,cdromedc,cksum,posix,iscsi,base91c,castagnoli,interlaken,c,nvme,jamcrc,mef,mpeg2,ether,xfer,koopman,k}] [-l] [--prefix PREFIX] [--suffix SUFFIX] [--prefix-hex PREFIX_HEX] [--suffix-hex SUFFIX_HEX]
                [--charset CHARSET] [-b BRIDGE_LENGTH] [-c] [-k IDX CHAR] [-K IDX HEX_CHAR] [-n]
                [WANTED_CRC]

positional arguments:
  WANTED_CRC            target CRC value (hex).

options:
  -h, --help            show this help message and exit
  -p, --poly POLY       generator polynomial in MSB form.
  --poly-reflected      treat --poly as already reflected (LSB form, e.g., 0xedb88320).
  -i, --init-value INIT_VALUE
                        initial CRC register value.
  -o, --xorout XOROUT   final XOR value applied after output reflection.
  --refin               enable input reflection (LSB-first).
  --no-refin            disable input reflection (MSB-first).
  --refout              enable output reflection.
  --no-refout           disable output reflection.
  --preset {,base,ieee,isohdlc,adccp,v42,xz,pkzip,aixm,q,autosar,base91d,d,bzip2,aal5,dectb,b,cdromedc,cksum,posix,iscsi,base91c,castagnoli,interlaken,c,nvme,jamcrc,mef,mpeg2,ether,xfer,koopman,k}
                        quick parameter presets, explicit flags override preset values.
  -l, --list            print CRC presets.
  --prefix PREFIX       prefix string (ASCII).
  --suffix SUFFIX       suffix string (ASCII).
  --prefix-hex PREFIX_HEX
                        prefix string (HEX).
  --suffix-hex SUFFIX_HEX
                        suffix string (HEX).
  --charset CHARSET     the character set for bruteforce (default: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_).
  -b, --bridge-length BRIDGE_LENGTH
                        specific bridge length.
  -c                    do not terminate midway.
  -k, --known IDX CHAR  specified known fixed value.
  -K, --known-hex IDX HEX_CHAR
                        specified known fixed value.
  -n, --no-pager        do not use the pager.
```

### Examples

```gdb
crc32rev --list
crc32rev 0x41414141
crc32rev 0x41414141 --prefix AAAA --suffix BBBB
crc32rev 0x41414141 --prefix flag{ --suffix-hex 7d00 -b 8 -k 1 A -k 3 A
crc32rev 0x41414141 --preset mpeg2
```

### Notes

```text
wanted_crc == crc(prefix + bridge + suffix).
```

## distance

Calculate the offset from its base address.


### Syntax

```text
usage: distance [-h] ADDRESS_A [ADDRESS_B]

positional arguments:
  ADDRESS_A   the address to calculate the offset as (A - base_addr_of(A)).
  ADDRESS_B   the address to calculate the offset as abs(A - B).

options:
  -h, --help  show this help message and exit
```

# 07-f. Misc - Diff
## diffo

The base command to diff of the command outputs.


### Syntax

```text
usage: diffo [-h] {colordiff,git-diff,list,clear} ...

options:
  -h, --help            show this help message and exit

command:
  {colordiff,git-diff,list,clear}
```

## diffo clear

Clear all saved outputs.


### Syntax

```text
usage: diffo clear [-h] [--all] [N ...]

positional arguments:
  N           index to be deleted.

options:
  -h, --help  show this help message and exit
  --all       delete everything.
```

## diffo colordiff

Diff the two outputs by colordiff.


### Syntax

```text
usage: diffo colordiff [-h] [-n] N M

positional arguments:
  N               first diff target got from `diffo list`.
  M               second diff target got from `diffo list`.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
diffo colordiff 0 1  # diff between 0 and 1
```

### Notes

```text
You can check the available indexes with `diffo list`.
```

## diffo git-diff

Diff the two outputs by git.


### Syntax

```text
usage: diffo git-diff [-h] [-n] N M

positional arguments:
  N               first diff target got from `diffo list`.
  M               second diff target got from `diffo list`.

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

### Examples

```gdb
diffo git-diff 0 1  # diff between 0 and 1
```

### Notes

```text
You can check the available indexes with `diffo list`.
```

## diffo list

List saved outputs.


### Syntax

```text
usage: diffo list [-h]

options:
  -h, --help  show this help message and exit
```

## saveo

Save the command outputs.


### Syntax

```text
usage: saveo [-h] GDB_CMD [ARG ...]

positional arguments:
  GDB_CMD     gdb command.
  ARG         arguments of gdb command.

options:
  -h, --help  show this help message and exit
```

### Notes

```text
Saving the output of external commands is unsupported (e.g., pipe, !ls).
```

# 07-g. Misc - Qemu-system
## qemu-system-memory-region-dump

Dump memory regions for qemu-system.


### Syntax

```text
usage: qemu-system-memory-region-dump [-h] [-s] [-n] [-q]

options:
  -h, --help      show this help message and exit
  -s, --smart     show only entries where read or write is not the default.
  -n, --no-pager  do not use the pager.
  -q, --quiet     enable quiet mode.
```

# 99. GEF Maintenance Command
## aliases

The base command to add, remove or list aliases.


### Syntax

```text
usage: aliases [-h] {add,rm,ls} ...

options:
  -h, --help   show this help message and exit

command:
  {add,rm,ls}
```

## aliases add

Add the command alias.


### Syntax

```text
usage: aliases add [-h] [-r] ALIAS COMMAND [COMMAND ...]

positional arguments:
  ALIAS         the name of new alias.
  COMMAND       the command of new alias.

options:
  -h, --help    show this help message and exit
  -r, --repeat  enforce repeat feature.
```

### Examples

```gdb
aliases add scope telescope
```

## aliases ls

List the command alias.


### Syntax

```text
usage: aliases ls [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## aliases rm

Remove the command alias.


### Syntax

```text
usage: aliases rm [-h] ALIAS

positional arguments:
  ALIAS       the name of alias to be deleted.

options:
  -h, --help  show this help message and exit
```

## gef

The base command of GEF maintenance.


### Syntax

```text
usage: gef [-h] {missing,config,save,restore,reload,reset-breakpoint,reset-cache,arch-list,raise-exception,pyobj-list,avail-comm-list,set-arch,status,version,check-update,tmux-setup,dump-commands} ...

options:
  -h, --help            show this help message and exit

command:
  {missing,config,save,restore,reload,reset-breakpoint,reset-cache,arch-list,raise-exception,pyobj-list,avail-comm-list,set-arch,status,version,check-update,tmux-setup,dump-commands}
```

## gef arch-list

Display defined architecture information.


### Syntax

```text
usage: gef arch-list [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## gef avail-comm-list

Display a list of commands available for the current architecture and gdb execution mode.


### Syntax

```text
usage: gef avail-comm-list [-h] [-s] [-a] [-u] [-n]

options:
  -h, --help            show this help message and exit
  -s, --sort            sort by command name.
  -a, --only-available  show only available commands.
  -u, --only-unavailable
                        show only unavailable commands.
  -n, --no-pager        do not use the pager.
```

## gef check-update

Check for gef updates.


### Syntax

```text
usage: gef check-update [-h]

options:
  -h, --help  show this help message and exit
```

## gef config

Display or change GEF configuration.


### Syntax

```text
usage: gef config [-h] [-s] [SETTING_NAME] [SETTING_VALUE]

positional arguments:
  SETTING_NAME          setting name.
  SETTING_VALUE         setting value.

options:
  -h, --help            show this help message and exit
  -s, --show-only-changes
                        show only changed settings.
```

## gef dump-commands

Dump GEF command documentation as Markdown.


### Syntax

```text
usage: gef dump-commands [-h] [OUTPUT]

positional arguments:
  OUTPUT      output file path. (default: COMMANDS.md)

options:
  -h, --help  show this help message and exit
```

## gef help

Display GEF command list.


### Syntax

```text
usage: gef help [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## gef missing

Display the GEF commands that could not be loaded with the reason.


### Syntax

```text
usage: gef missing [-h]

options:
  -h, --help  show this help message and exit
```

### Notes

```text
This command only detects commands that could not be loaded when GEF started.
To speed up startup, some commands lazy load required modules and dependencies.
These command cannot be detected.
```

## gef pyobj-list

Display defined global python object.


### Syntax

```text
usage: gef pyobj-list [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## gef raise-exception

Raise an exception for development.


### Syntax

```text
usage: gef raise-exception [-h]

options:
  -h, --help  show this help message and exit
```

## gef reload

Reload the GEF.


### Syntax

```text
usage: gef reload [-h]

options:
  -h, --help  show this help message and exit
```

## gef reset-breakpoint

Show and reset all breakpoints (include internal breakpoints).

- Alias: `reset-breakpoint`

### Syntax

```text
usage: gef reset-breakpoint [-h] [-c]

options:
  -h, --help    show this help message and exit
  -c, --commit  actually perform delete.
```

## gef reset-cache

Reset all caches (both Cache.cache_until_next and Cache.cache_this_session).

- Alias: `reset-cache`

### Syntax

```text
usage: gef reset-cache [-h] [--hard]

options:
  -h, --help  show this help message and exit
  --hard      also delete under /tmp/gef.
```

## gef restore

Load settings from '~/.gef.rc'.


### Syntax

```text
usage: gef restore [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## gef save

Save the current settings to '~/.gef.rc'.


### Syntax

```text
usage: gef save [-h] [-q]

options:
  -h, --help   show this help message and exit
  -q, --quiet  quiet execution.
```

## gef set-arch

Set a specific architecture to gef.


### Syntax

```text
usage: gef set-arch [-h] (-l | ARCH)

positional arguments:
  ARCH        target architecture.

options:
  -h, --help  show this help message and exit
  -l, --list  show supported architecture words.
```

## gef status

Display current gef status.

- Alias: `arch-info`

### Syntax

```text
usage: gef status [-h]

options:
  -h, --help  show this help message and exit
```

## gef tmux-setup

Setup a comfortable tmux environment.

- Alias: `tmux-setup`

### Syntax

```text
usage: gef tmux-setup [-h] [-r]

options:
  -h, --help   show this help message and exit
  -r, --reset  reset all panes.
```

### Notes

```text
- `screen` is no longer supported.

- `tmux` settings are predefined and cannot be customized in this command.
- If you want to customize it, edit `tmux_setup.py` and run `source /path/to/tmux_setup.py`.
- It can be found in https://github.com/bata24/gef/blob/dev/dev/tmux/tmux_setup.py.

- There is experimental support for `zellij` using a similar script.
- Try starting `zellij-wrapper.py` in your shell (before starting `zellij` and `gdb`).
- It can be found in https://github.com/bata24/gef/blob/dev/dev/zellij/zellij-wrapper.py.
```

## gef version

Display GEF version info.

- Alias: `version`

### Syntax

```text
usage: gef version [-h] [--compact]

options:
  -h, --help  show this help message and exit
  --compact   show compact style.
```

## history

Show gdb command history easily.


### Syntax

```text
usage: history [-h] [-n]

options:
  -h, --help      show this help message and exit
  -n, --no-pager  do not use the pager.
```

## theme

Customize GEF appearance.


### Syntax

```text
usage: theme [-h] [-c] [-n] [KEY] [VALUE ...]

positional arguments:
  KEY                 color theme key.
  VALUE               color theme value.

options:
  -h, --help          show this help message and exit
  -c, --color-sample  print available name of colors.
  -n, --no-pager      do not use the pager.
```

### Examples

```gdb
theme                         # show all theme settings
theme address_code            # show specified theme setting
theme address_code bold cyan  # set new theme
```

### Notes

```text
GDB 17 do not allow multiple color specifications (such as "bold red"). This bug had fixed in GDB 18.
```
