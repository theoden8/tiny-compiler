main() {
    int *n = 0xff;
    if(*n == 10)
        return n == 0xff;
    else
        return -1;
}
