#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    double x , y ;
} Point ;

typedef struct {
    Point a , b ;
} Segment ;

typedef struct No {
    struct No * esq ;
    struct No * dir ;
    struct No * pai ;
    Point p ;
    int id ;
} No ;
typedef No * ptrNo ;

void salvarPontosCSV(Point *pontos, int n)
{
    FILE *fp = fopen("pontos.csv", "w");

    if(fp == NULL)
    {
        printf("Erro ao criar o arquivo pontos.csv\n");
        return;
    }

    fprintf(fp,"id,x,y\n");

    for(int i = 0; i < n; i++)
    {
        fprintf(fp,"%d,%lf,%lf\n",
                i + 1,
                pontos[i].x,
                pontos[i].y);
    }

    fclose(fp);

    printf("\nArquivo pontos.csv criado com sucesso!\n");
}

ptrNo criarNo (Point p, int id, ptrNo pai)
{
    ptrNo novo = (ptrNo) malloc(sizeof(No));
    if (novo == NULL)
    {
        printf("Erro de alocacao!\n");
        exit(1);
    }
    
    novo->id = id;
    novo->p = p;
    novo->pai = pai;
    novo->dir = NULL;
    novo->esq = NULL;

    return novo;
}

double randomDouble(double min, double max)
{
    return min + (max - min) * ((double) rand() / RAND_MAX);
}

Point gerarPonto(double raio)
{
    Point p;
    do
    {
       p.x = randomDouble(-raio, raio);
       p.y = randomDouble(-raio, raio);
    } while (p.x*p.x + p.y*p.y > raio*raio);

    return p;

}
int main(int argc, char *argv[])
{
    if(argc != 3){
        printf("Numero de argumentos invalidos. Tente Novamente");
        return 1;
    }
    int Nterm = atoi(argv[1]);
    double R = atof(argv[2]);
    
    srand(time(NULL));

    //criando ponto raiz 
    Point centro;
    centro.x = 0.0;
    centro.y = 0.0;

    ptrNo raiz = criarNo(centro, 0, NULL);

    Point *terminais;

    terminais = (Point *) malloc(Nterm*sizeof(Point));

    if(terminais == NULL)
    {
        printf("Erro de alocacao.\n");
        return 1;
    }

    //criando novos vizinhos 
    for(int i = 0; i <Nterm; i++)
    {
        terminais[i] = gerarPonto(R);
    }

    salvarPontosCSV(terminais, Nterm);

    free(terminais);
    free(raiz);
    return 0;
    
}