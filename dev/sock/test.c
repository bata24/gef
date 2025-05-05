#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/un.h>
#include <errno.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/icmp6.h>

#define PORT_TCP4 5001
#define PORT_TCP6 5002
#define PORT_UDP4 5003
#define PORT_UDP6 5004
#define UNIX_SOCK_PATH "/tmp/echo_unix.sock"
#define BUFFER_SIZE 1024

char* bytes_to_hex(const unsigned char* bytes, size_t len) {
    if (bytes == NULL || len == 0) {
        return NULL;
    }
    size_t hex_len = len * 2 + 1;
    char* hex_str = (char*)malloc(hex_len);
    if (hex_str == NULL) {
        perror("malloc failed");
        return NULL;
    }
    for (size_t i = 0; i < len; ++i) {
        sprintf(hex_str + (i * 2), "%02X", bytes[i]);
    }
    hex_str[hex_len - 1] = '\0';
    return hex_str;
}

void *tcp4_echo_server(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    printf("[DEBUG] tcp4_server socket: fd=%d\n", server_fd);
    if (server_fd < 0) { perror("tcp4 socket"); exit(1); }
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT_TCP4);
    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("tcp4 bind"); exit(1);
    }
    if (listen(server_fd, 3) < 0) { perror("tcp4 listen"); exit(1); }

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("[DEBUG] tcp4_server accept: fd=%d\n", client_fd);
        if (client_fd < 0) { perror("tcp4 accept"); continue; }
        char buffer[BUFFER_SIZE];
        int valread;
        while ((valread = read(client_fd, buffer, BUFFER_SIZE)) > 0) {
            write(client_fd, buffer, valread);
        }
        close(client_fd);
        printf("[DEBUG] tcp4_server close client: fd=%d\n", client_fd);
    }
    return NULL;
}

void *tcp6_echo_server(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_in6 addr;
    server_fd = socket(AF_INET6, SOCK_STREAM, 0);
    printf("[DEBUG] tcp6_server socket: fd=%d\n", server_fd);
    if (server_fd < 0) { perror("tcp6 socket"); exit(1); }
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any;
    addr.sin6_port = htons(PORT_TCP6);
    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("tcp6 bind"); exit(1);
    }
    if (listen(server_fd, 3) < 0) { perror("tcp6 listen"); exit(1); }

    while (1) {
        struct sockaddr_in6 client_addr;
        socklen_t addrlen = sizeof(client_addr);
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("[DEBUG] tcp6_server accept: fd=%d\n", client_fd);
        if (client_fd < 0) { perror("tcp6 accept"); continue; }
        char buffer[BUFFER_SIZE];
        int valread;
        while ((valread = read(client_fd, buffer, BUFFER_SIZE)) > 0) {
            write(client_fd, buffer, valread);
        }
        close(client_fd);
        printf("[DEBUG] tcp6_server close client: fd=%d\n", client_fd);
    }
    return NULL;
}

void *udp4_server(void *arg) {
    int sockfd;
    struct sockaddr_in addr;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    printf("[DEBUG] udp4_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("udp4 socket"); exit(1); }
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT_UDP4);
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("udp4 bind"); exit(1);
    }

    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&client_addr, &addrlen);
        if (n < 0) { perror("udp4 recvfrom"); continue; }
        // 何もしない
        printf("[udp4 srever] %s", buffer);
    }
    return NULL;
}

void *udp6_server(void *arg) {
    int sockfd;
    struct sockaddr_in6 addr;
    sockfd = socket(AF_INET6, SOCK_DGRAM, 0);
    printf("[DEBUG] udp6_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("udp6 socket"); exit(1); }
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any;
    addr.sin6_port = htons(PORT_UDP6);
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("udp6 bind"); exit(1);
    }

    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in6 client_addr;
        socklen_t addrlen = sizeof(client_addr);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&client_addr, &addrlen);
        if (n < 0) { perror("udp6 recvfrom"); continue; }
        printf("[udp6 server] %s", buffer);
    }
    return NULL;
}

void *unix_echo_server(void *arg) {
    int server_fd, client_fd;
    struct sockaddr_un addr;
    unlink(UNIX_SOCK_PATH);
    server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    printf("[DEBUG] unix_server socket: fd=%d\n", server_fd);
    if (server_fd < 0) { perror("unix socket"); exit(1); }
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, UNIX_SOCK_PATH, sizeof(addr.sun_path)-1);
    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("unix bind"); exit(1);
    }
    if (listen(server_fd, 3) < 0) { perror("unix listen"); exit(1); }

    while (1) {
        client_fd = accept(server_fd, NULL, NULL);
        printf("[DEBUG] unix_server accept: fd=%d\n", client_fd);
        if (client_fd < 0) { perror("unix accept"); continue; }
        char buffer[BUFFER_SIZE];
        int valread;
        while ((valread = read(client_fd, buffer, BUFFER_SIZE)) > 0) {
            write(client_fd, buffer, valread);
        }
        close(client_fd);
        printf("[DEBUG] unix_server close client: fd=%d\n", client_fd);
    }
    return NULL;
}

void *icmp_server(void *arg) {
    int sockfd;
    struct sockaddr_in addr;
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    printf("[DEBUG] icmp_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("icmp socket (要root)"); pthread_exit(NULL); }
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("icmp bind"); pthread_exit(NULL);
    }
    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in from;
        socklen_t fromlen = sizeof(from);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&from, &fromlen);
        if (n < 0) { perror("icmp recvfrom"); continue; }
        printf("[icmp4 server] %s\n", bytes_to_hex(buffer, n));
        fflush(stdout);
    }
    return NULL;
}

void *icmp6_server(void *arg) {
    int sockfd;
    struct sockaddr_in6 addr;
    sockfd = socket(AF_INET6, SOCK_RAW, IPPROTO_ICMPV6);
    printf("[DEBUG] icmp6_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("icmp6 socket (要root)"); pthread_exit(NULL); }
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any;
    addr.sin6_port = 0;
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("icmp6 bind"); pthread_exit(NULL);
    }
    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in6 from;
        socklen_t fromlen = sizeof(from);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&from, &fromlen);
        if (n < 0) { perror("icmp6 recvfrom"); continue; }
        printf("[icmp6 server] %s\n", bytes_to_hex(buffer, n));
        fflush(stdout);
    }
    return NULL;
}

void *raw_server(void *arg) {
    int sockfd;
    struct sockaddr_in addr;
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    printf("[DEBUG] raw_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("raw socket (要root)"); pthread_exit(NULL); }
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("raw bind"); pthread_exit(NULL);
    }
    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in from;
        socklen_t fromlen = sizeof(from);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&from, &fromlen);
        if (n < 0) { perror("raw recvfrom"); continue; }
        printf("[raw server] %s", buffer);
        fflush(stdout);
    }
    return NULL;
}

void *raw6_server(void *arg) {
    int sockfd;
    struct sockaddr_in6 addr;
    sockfd = socket(AF_INET6, SOCK_RAW, IPPROTO_RAW);
    printf("[DEBUG] raw6_server socket: fd=%d\n", sockfd);
    if (sockfd < 0) { perror("raw6 socket (要root)"); pthread_exit(NULL); }
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any;
    addr.sin6_port = 0;
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("raw6 bind"); pthread_exit(NULL);
    }
    while (1) {
        char buffer[BUFFER_SIZE];
        struct sockaddr_in6 from;
        socklen_t fromlen = sizeof(from);
        ssize_t n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&from, &fromlen);
        if (n < 0) { perror("raw6 recvfrom"); continue; }
        printf("[raw6 server] %s", buffer);
        fflush(stdout);
    }
    return NULL;
}

void *client_thread(void *arg) {
    int sock4 = socket(AF_INET, SOCK_STREAM, 0);
    printf("[DEBUG] client tcp4 socket: fd=%d\n", sock4);
    if (sock4 < 0) { perror("client tcp4 socket"); exit(1); }
    struct sockaddr_in addr4;
    addr4.sin_family = AF_INET;
    addr4.sin_port = htons(PORT_TCP4);
    inet_pton(AF_INET, "127.0.0.1", &addr4.sin_addr);
    if (connect(sock4, (struct sockaddr *)&addr4, sizeof(addr4)) < 0) {
        perror("client tcp4 connect"); exit(1);
    }

    int sock6 = socket(AF_INET6, SOCK_STREAM, 0);
    printf("[DEBUG] client tcp6 socket: fd=%d\n", sock6);
    if (sock6 < 0) { perror("client tcp6 socket"); exit(1); }
    struct sockaddr_in6 addr6;
    addr6.sin6_family = AF_INET6;
    addr6.sin6_port = htons(PORT_TCP6);
    inet_pton(AF_INET6, "::1", &addr6.sin6_addr);
    if (connect(sock6, (struct sockaddr *)&addr6, sizeof(addr6)) < 0) {
        perror("client tcp6 connect"); exit(1);
    }

    int usock4 = socket(AF_INET, SOCK_DGRAM, 0);
    printf("[DEBUG] client udp4 socket: fd=%d\n", usock4);
    if (usock4 < 0) { perror("client udp4 socket"); exit(1); }
    struct sockaddr_in uaddr4;
    uaddr4.sin_family = AF_INET;
    uaddr4.sin_port = htons(PORT_UDP4);
    inet_pton(AF_INET, "127.0.0.1", &uaddr4.sin_addr);

    int usock6 = socket(AF_INET6, SOCK_DGRAM, 0);
    printf("[DEBUG] client udp6 socket: fd=%d\n", usock6);
    if (usock6 < 0) { perror("client udp6 socket"); exit(1); }
    struct sockaddr_in6 uaddr6;
    uaddr6.sin6_family = AF_INET6;
    uaddr6.sin6_port = htons(PORT_UDP6);
    inet_pton(AF_INET6, "::1", &uaddr6.sin6_addr);

    int unix_sock = socket(AF_UNIX, SOCK_STREAM, 0);
    printf("[DEBUG] client unix socket: fd=%d\n", unix_sock);
    if (unix_sock < 0) { perror("client unix socket"); exit(1); }
    struct sockaddr_un unix_addr;
    memset(&unix_addr, 0, sizeof(unix_addr));
    unix_addr.sun_family = AF_UNIX;
    strncpy(unix_addr.sun_path, UNIX_SOCK_PATH, sizeof(unix_addr.sun_path)-1);
    while (connect(unix_sock, (struct sockaddr *)&unix_addr, sizeof(unix_addr)) < 0) {
        if (errno == ENOENT) { usleep(100000); continue; }
        perror("client unix connect");
        exit(1);
    }

    int icmp_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    printf("[DEBUG] client icmp socket: fd=%d\n", icmp_sock);
    struct sockaddr_in icmp_addr;
    icmp_addr.sin_family = AF_INET;
    inet_pton(AF_INET, "127.0.0.1", &icmp_addr.sin_addr);

    int icmp6_sock = socket(AF_INET6, SOCK_RAW, IPPROTO_ICMPV6);
    printf("[DEBUG] client icmp6 socket: fd=%d\n", icmp6_sock);
    struct sockaddr_in6 icmp6_addr;
    icmp6_addr.sin6_family = AF_INET6;
    inet_pton(AF_INET6, "::1", &icmp6_addr.sin6_addr);

    int raw_sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    printf("[DEBUG] client raw socket: fd=%d\n", raw_sock);
    struct sockaddr_in raw_addr;
    raw_addr.sin_family = AF_INET;
    inet_pton(AF_INET, "127.0.0.1", &raw_addr.sin_addr);

    int raw6_sock = socket(AF_INET6, SOCK_RAW, IPPROTO_RAW);
    printf("[DEBUG] client raw6 socket: fd=%d\n", raw6_sock);
    struct sockaddr_in6 raw6_addr;
    raw6_addr.sin6_family = AF_INET6;
    inet_pton(AF_INET6, "::1", &raw6_addr.sin6_addr);

    while (1) {
        char input[BUFFER_SIZE];
        sleep(0.1);
        printf("Input: ");
        if (!fgets(input, BUFFER_SIZE, stdin)) break;

        send(sock4, input, strlen(input), 0);
        char resp4[BUFFER_SIZE] = {0};
        int r4 = read(sock4, resp4, BUFFER_SIZE-1);
        if (r4 > 0) resp4[r4] = '\0';
        printf("[TCPv4 echo] %s", resp4);

        send(sock6, input, strlen(input), 0);
        char resp6[BUFFER_SIZE] = {0};
        int r6 = read(sock6, resp6, BUFFER_SIZE-1);
        if (r6 > 0) resp6[r6] = '\0';
        printf("[TCPv6 echo] %s", resp6);

        sendto(usock4, input, strlen(input), 0, (struct sockaddr *)&uaddr4, sizeof(uaddr4));
        sendto(usock6, input, strlen(input), 0, (struct sockaddr *)&uaddr6, sizeof(uaddr6));

        send(unix_sock, input, strlen(input), 0);
        char unix_resp[BUFFER_SIZE] = {0};
        int ur = read(unix_sock, unix_resp, BUFFER_SIZE-1);
        if (ur > 0) unix_resp[ur] = '\0';
        printf("[UNIX echo] %s", unix_resp);

        if (icmp_sock >= 0) {
            char icmp_packet[8] = {8, 0, 0, 0, 0, 0, 0, 0};
            sendto(icmp_sock, icmp_packet, sizeof(icmp_packet), 0, (struct sockaddr *)&icmp_addr, sizeof(icmp_addr));
        }
        if (icmp6_sock >= 0) {
            char icmp6_packet[8] = {128, 0, 0, 0, 0, 0, 0, 0};
            sendto(icmp6_sock, icmp6_packet, sizeof(icmp6_packet), 0, (struct sockaddr *)&icmp6_addr, sizeof(icmp6_addr));
        }
        if (raw_sock >= 0) {
            char raw_data[BUFFER_SIZE] = "RAW DATA";
            sendto(raw_sock, raw_data, strlen(raw_data), 0, (struct sockaddr *)&raw_addr, sizeof(raw_addr));
        }
        if (raw6_sock >= 0) {
            char raw6_data[BUFFER_SIZE] = "RAW6 DATA";
            sendto(raw6_sock, raw6_data, strlen(raw6_data), 0, (struct sockaddr *)&raw6_addr, sizeof(raw6_addr));
        }
    }

    close(sock4);
    close(sock6);
    close(usock4);
    close(usock6);
    close(unix_sock);
    if (icmp_sock >= 0) close(icmp_sock);
    if (icmp6_sock >= 0) close(icmp6_sock);
    if (raw_sock >= 0) close(raw_sock);
    if (raw6_sock >= 0) close(raw6_sock);
    return NULL;
}

int main() {
    pthread_t threads[10];
    pthread_create(&threads[0], NULL, tcp4_echo_server, NULL);
    pthread_create(&threads[1], NULL, tcp6_echo_server, NULL);
    pthread_create(&threads[2], NULL, udp4_server, NULL);
    pthread_create(&threads[3], NULL, udp6_server, NULL);
    pthread_create(&threads[4], NULL, unix_echo_server, NULL);
    pthread_create(&threads[5], NULL, icmp_server, NULL);
    pthread_create(&threads[6], NULL, icmp6_server, NULL);
    pthread_create(&threads[7], NULL, raw_server, NULL);
    pthread_create(&threads[8], NULL, raw6_server, NULL);
    pthread_create(&threads[9], NULL, client_thread, NULL);

    for (int i = 0; i < 10; ++i) {
        pthread_join(threads[i], NULL);
    }
    return 0;
}
