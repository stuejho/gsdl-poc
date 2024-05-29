M=
N=

CFLAGS=-std=c99 -O2
CFLAGS_DEBUG=-std=c99 -g -O0 -DDEBUG

all: build

build:
	gcc $(CFLAGS_DEBUG) -DM=$(M) -DN=$(N) \
		-c baseline.c -o baseline.o
	gcc $(CFLAGS_DEBUG) -DM=$(M) -DN=$(N) \
		-c benchmark.c -o benchmark.o
	gcc $(CFLAGS_DEBUG) \
		-c main.c -o main.o
	gcc $(CFLAGS_DEBUG) -DM=$(M) -DN=$(N) \
		-c util.c -o util.o
	gcc $(CFLAGS_DEBUG) \
		baseline.o benchmark.o main.o util.o -o ./main.x -lm

clean:
	rm -f *.o *.x *~ *.s
