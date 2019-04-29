#include <stdio.h>
#include <pcap.h>
#include <time.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <string.h>

void pcap_callback(unsigned char *arg, const struct pcap_pkthdr *packet_header, const unsigned char *packet_content)
{
    int *id = (int *)arg; //记录包ID
    printf("id=%d\n", ++(*id));

    printf("Packet length : %d\n", packet_header->len);
    printf("Number of bytes : %d\n", packet_header->caplen);
    printf("Received time : %s\n", ctime((const time_t *)&packet_header->ts.tv_sec));
    int i;
    for (i = 0; i < packet_header->caplen; i++)
    {
        printf(" %02x", packet_content[i]);
        if ((i + 1) % 16 == 0)
        {
            printf("\n");
        }
    }
    printf("\n\n");
}

int main(int argc, char const *argv[])
{
    char *dev, errbuf[1024];

    dev = pcap_lookupdev(errbuf);

    if (dev == NULL)
    {
        printf("%s\n", errbuf);
        return 0;
    }

    printf("Device: %s\n", dev);

    pcap_t *pcap_handle = pcap_open_live(dev, 65535, 1, 0, errbuf);

    if (pcap_handle == NULL)
    {
        printf("%s\n", errbuf);
        return 0;
    }

    struct in_addr addr;
    bpf_u_int32 ipaddress, ipmask;
    char *dev_ip, *dev_mask;

    if (pcap_lookupnet(dev, &ipaddress, &ipmask, errbuf) == -1)
    {
        printf("%s\n", errbuf);
        return 0;
    }

    //输出ip
    addr.s_addr = ipaddress;
    dev_ip = inet_ntoa(addr);
    printf("ip address : %s\n", dev_ip);
    //输出掩码
    addr.s_addr = ipmask;
    dev_mask = inet_ntoa(addr);
    printf("netmask : %s\n", dev_mask);

    printf("------Package------\n");
    int id = 0;
    if (pcap_loop(pcap_handle, 10, pcap_callback, (unsigned char *)&id) < 0)
    { //接收十个数据包
        printf("error\n");
        return 0;
    }
    pcap_close(pcap_handle);
    return 0;
}
