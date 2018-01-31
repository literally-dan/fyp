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

    printf("%s\n",dev_name);

    if(*dev_name){ //if a name is provided, set it
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

int safe_write(int tun, char* buf, int n){
    int write_count;
    
    write_count = write (tun,buf,n);

    if(write_count < 0){
        perror("writing data to tun");
        exit(write_count);
    }

    return write_count;
}
int safe_read(int tun, char* buf, int n){
    int read_count;

    read_count = read(tun,buf,n);

    if(read_count < 0){
        perror("Reading data from tun");
        exit(read_count);
    }

    return read_count;
}

int read_n(int fd, char *buffer, int to_read) {

  int read_count;
  int remaining = to_read;

  while(remaining > 0) {
    if ((read_count = safe_read(fd, buffer, remaining))==0){
      return 0;
    }else {
      remaining -= read_count;
      buffer += read_count;
    }
  }
  return to_read;
}
