//-----------------------------------------------------------------------------
// Utility functions that depend on Win32. Notably, our memory allocation;
// we use two separate allocators, one for long-lived stuff and one for
// stuff that gets freed after every regeneration of the model, to save us
// the trouble of freeing the latter explicitly.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------
#ifdef WIN32
#   include <windows.h>
#endif
#include <stdarg.h>
#include <string.h>
#include <stdio.h>

#include "solvespace.h"

#ifdef WIN32

static HANDLE PermHeap, TempHeap;

void dbp(char *str, ...)
{
    va_list f;
    static char buf[1024*50];
    va_start(f, str);
    _vsnprintf(buf, sizeof(buf), str, f);
    va_end(f);

    OutputDebugString(buf);
}

void GetAbsoluteFilename(char *file)
{
    char absoluteFile[MAX_PATH];
    GetFullPathName(file, sizeof(absoluteFile), absoluteFile, NULL);
    strcpy(file, absoluteFile);
}

//-----------------------------------------------------------------------------
// A separate heap, on which we allocate expressions. Maybe a bit faster,
// since no fragmentation issues whatsoever, and it also makes it possible
// to be sloppy with our memory management, and just free everything at once
// at the end.
//-----------------------------------------------------------------------------
void *AllocTemporary(int n)
{
    void *v = HeapAlloc(TempHeap, HEAP_NO_SERIALIZE | HEAP_ZERO_MEMORY, n);
    if(!v) oops();
    return v;
}
void FreeTemporary(void *p) {
    HeapFree(TempHeap, HEAP_NO_SERIALIZE, p);
}
void FreeAllTemporary(void)
{
    if(TempHeap) HeapDestroy(TempHeap);
    TempHeap = HeapCreate(HEAP_NO_SERIALIZE, 1024*1024*20, 0);
    // This is a good place to validate, because it gets called fairly
    // often.
    vl();
}

void *MemRealloc(void *p, int n) {
    if(!p) {
        return MemAlloc(n);
    }

    p = HeapReAlloc(PermHeap, HEAP_NO_SERIALIZE | HEAP_ZERO_MEMORY, p, n);
    if(!p) oops();
    return p;
}
void *MemAlloc(int n) {
    void *p = HeapAlloc(PermHeap, HEAP_NO_SERIALIZE | HEAP_ZERO_MEMORY, n);
    if(!p) oops();
    return p;
}
void MemFree(void *p) {
    HeapFree(PermHeap, HEAP_NO_SERIALIZE, p);
}

void vl(void) {
    if(!HeapValidate(TempHeap, HEAP_NO_SERIALIZE, NULL)) oops();
    if(!HeapValidate(PermHeap, HEAP_NO_SERIALIZE, NULL)) oops();
}

void InitHeaps(void) {
    // Create the heap used for long-lived stuff (that gets freed piecewise).
    PermHeap = HeapCreate(HEAP_NO_SERIALIZE, 1024*1024*20, 0);
    // Create the heap that we use to store Exprs and other temp stuff.
    FreeAllTemporary();
}

#else   // not WIN32

#include <stdlib.h>
// not available without support for C++0x
// I could enable that, but I rather use the old, portable way.
//#include <unordered_set>
#include <set>

void dbp(char *str, ...)
{
    va_list f;
    static char buf[1024*50];
    va_start(f, str);
    vsnprintf(buf, sizeof(buf), str, f);
    va_end(f);

    fprintf(stderr, "%s", buf);
}

void GetAbsoluteFilename(char *file)
{
    char* absoluteFile = realpath(file, NULL);
    if (strlen(absoluteFile) > MAX_PATH-1) {
        printf("This absolute path is too long: %s\nI will quit now. Sorry.\n", absoluteFile);
        exit(2);
    }
    strcpy(file, absoluteFile);
}

// We're using the default heap here, so the 'free' trick (see above)
// doesn't work. This means that we might leak a lot of memory.
// Therefore, we keep track of temporary stuff and free it in
// FreeAllTemporary. Of course, we must 'forget' any pointer that
// has been deleted with FreeTemporary, so we don't free it again.

typedef std::set<void*> tmem;
tmem temporary_memory;

void *AllocTemporary(int n) {
    void *p = MemAlloc(n);
    temporary_memory.insert(p);
    return p;
}
void FreeTemporary(void *p) {
    temporary_memory.erase(p);
    MemFree(p);
}
void FreeAllTemporary(void) {
    for (typename tmem::iterator i = temporary_memory.begin();
         i != temporary_memory.end();
         i++) {
        MemFree(*i);
    }
    temporary_memory.clear();

    vl();
}

void *MemRealloc(void *p, int n) {
    if(!p) {
        return MemAlloc(n);
    }

    void *p2 = realloc(p, n);
    if(!p2) oops();
    //TODO initialize additional memory with zeros

    if (p != p2) {
        temporary_memory.erase(p);
        temporary_memory.insert(p2);
    }

    return p2;
}
void *MemAlloc(int n) {
    void* x = malloc(n);
    memset(x, 0, n);
    return x;
}
void MemFree(void *p) {
    free(p);
}

void vl(void) {
    // we cannot validate resp. stdlib does it automatically at
    // appropriate times, if we have compiled it for debug
}

void InitHeaps(void) {
}

#endif
