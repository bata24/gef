#include <stdio.h>
#include <string.h>
int main(int argc, char* argv[]) {
  if (argc != 2)
    return 0;

  if (memcmp(argv[1], "hogehoge", 8) == 0) {
    puts("ok");
  }
  return 0;
}
