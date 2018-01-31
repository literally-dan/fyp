#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/if.h>
#include <string.h>
#include <linux/if_tun.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <stddef.h>
#include <unistd.h>



int get_tun(char * dev_name, int flags){
    struct ifreq ifr;
    int tun;
    int error;

    tun = open("/dev/net/tun", O_RDWR); //create tun/tap dev_name

    if(tun < 0){
        perror("opening /dev/net/tun"); //if unable to create return an error
        return tun;
    }

    memset(&ifr, 0, sizeof(ifr)); //set the contents of IFR to 0's

    ifr.ifr_flags = flags; //set the flags

    if(*dev_name != 0){ //if a name is provided, set it
        strncpy(ifr.ifr_name,dev_name, IFNAMSIZ);
    }

    error = ioctl(tun,TUNSETIFF, &ifr);

    if(error < 0){
        perror("Could not set flags with ioctl on tun interface");
        close(tun);
        return error;
    }

    strncpy(dev_name,ifr.ifr_name,IFNAMSIZ); //set the name from ifr back to the string passed in

    return tun;

}

int set_tun_persistent(int tun,int persist){
    int ret = ioctl(tun,TUNSETPERSIST,persist);
    if(ret < 0){
        perror("Failed to change tun persistence");
        return ret;
    }
    return 0;
}

int main(){
    char * dev_name = malloc(sizeof(char)*IFNAMSIZ);
    int flags = IFF_TUN | IFF_NO_PI;

    int tun = get_tun(dev_name,flags);
    if(tun < 0){
        exit(tun);
    }

    int persist = set_tun_persistent(tun,1);


}
