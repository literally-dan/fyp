.PHONY: all clean

CC = gcc
CFLAGS = -D_GNU_SOURCE -Wall -Wextra -Werror -pedantic -std=c11 -pthread -O0 -g -Wno-unused-variable -Wno-unused-parameter -Wno-unused-function -Wno-unused-but-set-variable
SOURCE = $(wildcard *.c) #all .c files
HEADER = $(SOURCE:.c=.h)
OBJS = $(SOURCE:.c=.o)
TARGET = $(SOURCE:.c=)

all: $(TARGET) $(OBJS)

clean:
	rm -f $(OBJS) $(TARGET)

%: %.o
	$(CC) $(CFLAGS) -o $@ $<

%.o: %.c
	$(CC) -c $(CFLAGS) $<
