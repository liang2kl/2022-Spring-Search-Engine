#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ITERATIONS 100
#define MAX_ENTRIES 30000000UL
#define MAX_LINES 1109153UL

#ifdef _DEBUG
#define ALPHA 0.2
#else
#define ALPHA 0.15
#endif

struct node {
    int val;
    int next;
};

struct node *pool;
long *entries;
int *out_degrees;
int *valid_nodes;
double *pr;
double *I;

unsigned long cursor = 0;

void insert(int to, int from) {
    struct node *new_node = &pool[cursor];
    new_node->val = to;
    new_node->next = entries[from];
    entries[from] = cursor;
    cursor++;
}

int main() {
#ifdef _DEBUG
    freopen("wiki.graph", "r", stdin);
#endif

    pool = malloc(MAX_LINES * 1000 * sizeof(struct node));
    entries = malloc(MAX_ENTRIES * sizeof(long));
    out_degrees = malloc(MAX_ENTRIES * sizeof(int));
    valid_nodes = malloc(MAX_ENTRIES * sizeof(int));
    pr = malloc(MAX_ENTRIES * sizeof(double));
    I = malloc(MAX_ENTRIES * sizeof(double));

    if (!pool || !entries || !out_degrees || !valid_nodes || !pr || !I) {
        puts("fail to allocate memory");
        return 1;
    }

    for (int i = 0; i < MAX_ENTRIES; i++) {
        entries[i] = -1;
        out_degrees[i] = 0;
    }

    char *line = NULL;
    size_t len = 0;

    int entry_num = 0;

    char *head_str, *out_str;
    int head, out;

    while (getline(&line, &len, stdin) != -1) {
        head_str = strsep(&line, ":");
        head = atoi(head_str);

        if (entries[head] == -1) {
            entries[head] = -2;
            entry_num++;
        }

        while ((out_str = strsep(&line, ","))) {
            if (*out_str == '\0' || *out_str == '\n') {
                break;
            }
            out = atoi(out_str);
            insert(out, head);
            out_degrees[head]++;

            // mark as exist
            if (entries[out] == -1) {
                entries[out] = -2;
                entry_num++;
            }
        }
    }

    double s = 0;

    int valid_cursor = 0;

    double pr_init = 1 / entry_num;
    double i_init = ALPHA / entry_num;

    for (int i = 0; i < MAX_ENTRIES; i++) {
        if (entries[i] >= 0 || entries[i] == -2) {
            valid_nodes[valid_cursor] = i;
            valid_cursor++;

            pr[i] = pr_init;
            I[i] = i_init;
        }
    }

    for (int k = 0; k < ITERATIONS; k++) {
        s = 0;

        for (int j = 0; j < valid_cursor; j++) {
            int i = valid_nodes[j];
            int out = entries[i];

            if (out < 0) {
                s += pr[i];
                continue;
            }
            double score = (1 - ALPHA) * pr[i] / out_degrees[i];
            while (out >= 0) {
                I[pool[out].val] += score;
                out = pool[out].next;
            }
        }

        double pr_delta = (1 - ALPHA) * s / entry_num;

        for (int j = 0; j < valid_cursor; j++) {
            int i = valid_nodes[j];

            pr[i] = I[i] + pr_delta;
            I[i] = i_init;
        }
    }

    for (int j = 0; j < valid_cursor; j++) {
        int i = valid_nodes[j];
        if (entries[i] == -2 || entries[i] >= 0) {
            printf("%d %.10f\n", i, pr[i]);
        }
    }
}
