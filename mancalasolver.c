#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* returns the greater of two integers */
int max(int a, int b){
	return(a > b ? a : b);
}

void printboard(int* board){
	printf(" %i \n",board[13]);
	printf("%i %i\n",board[0],board[12]);
	printf("%i %i\n",board[1],board[11]);
	printf("%i %i\n",board[2],board[10]);
	printf("%i %i\n",board[3],board[9]);
	printf("%i %i\n",board[4],board[8]);
	printf("%i %i\n",board[5],board[7]);
	printf(" %i \n",board[6]);
}

int tap(int* board, int move, int m1, int m2, int m3, int m4, int m5, int m6){
	if(board[move] == 0){
		//printf("invalid move\n");
		return board[6];
	}
	int b = move;
	int a = 0;
	int storage = board[move];
	board[move] = 0;
	for(a = 0; a < storage; a++){
		b = (b + 1) % 13;
		board[b] += 1;
	}
	if((move + a) % 13 == 6){
		tap(board,m1,m2,m3,m4,m5,m6,1);
		//printf("go again\n");
	}else if(board[(move + a) % 13] > 1){
		tap(board,board[(move + a) % 13],m1,m2,m3,m4,m5,m6);
	}
	//printf("not your turn anymore\n");
	//printf("your score: %i\n",board[6]);
	return board[6];
}

/* does not repeat turn on base hit */
int tap2(int* board, int move){
	if(board[move] == 0){
		//printf("invalid move\n");
		return board[6];
	}
	int b = move;
	int a = 0;
	int storage = board[move];
	board[move] = 0;
	for(a = 0; a < storage; a++){
		b = (b + 1) % 13;
		board[b] += 1;
	}
	if((move + a) % 13 == 6){
		return board[6];
	}else if(board[(move + a) % 13] > 1){
		tap2(board,board[(move + a) % 13]);
	}
	//printf("not your turn anymore\n");
	//printf("your score: %i\n",board[6]);
	return board[6];
}

void resetboard(int *board){
	/*for(int a = 0; a < 13; a++){
		board[a] = 4;
	}*/
	 board[0] = 0;
	 board[1] = 1;
	 board[2] = 2;
	 board[3] = 1;
	 board[4] = 12;
	 board[5] = 2;
	 board[6] = 2; // your base
	 board[7] = 1;
	 board[8] = 0;
	 board[9] = 0;
	board[10] = 3;
	board[11] = 2;
	board[12] = 1;
	board[13] = 11; // opposing base
}

int main(int argc, char **argv){
	int *board = malloc(200000);
	int bestscore = 0;
	int lastbestscore = 0;
	int bestb, bestc, bestd, beste, bestf, bestg, besth;
	for(int b = 0; b < 6; b++){
		for(int c = 0; c < 6; c++){
			for(int d = 0; d < 6; d++){
				for(int e = 0; e < 6; e++){
					for(int f = 0; f < 6; f++){
						for(int g = 0; g < 6; g++){
							for(int h = 0; h < 6; h++){
								resetboard(board);
								bestscore = max(bestscore,tap(board,b,c,d,e,f,g,h));
								if(bestscore > lastbestscore){
									bestb = b;
									bestc = c;
									bestd = d;
									beste = e;
									bestf = f;
									bestg = g;
									besth = h;
								}
								lastbestscore = bestscore;
								//printboard(board);
							}
						}
					}
				}
			}
		}
	}
	printf("best score: %i\n",bestscore);
	resetboard(board);
	tap(board,bestb,bestc,bestd,beste,bestf,bestg,besth);
	//tap2(board,bestb);
	printf("b: %i, c: %i, d: %i, e: %i, f: %i, g: %i, h: %i\n",
	bestb,bestc,bestd,beste,bestf,bestg,besth);
	printboard(board);
	free(board);
}