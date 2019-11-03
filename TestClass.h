#ifndef TestClass_h
#define TestClass_h

#include <stuff>

void globalFuncDec(int arg1, int arg2);

class TestClass {
    struct defaultSpecifier {
        int x;
        int y;
    };
    private:
    class privateSpecifier {
        int x;
        int y; 
    };
    class parentClass {
        int x;
        int y;
        class childPrivateClass {
            int x;
        };
	public:
	class childPublicClass {
	    int x;
	};
    };
    
    class emptyClass { };
    
    public:
    void publicFunction(int x, int y);
    void publicFunctionNoArgs();

    struct publicStruct{ 
        int x;
        int y;
    };
    enum enum1 {
        int x;
        int y;
    };
    private:
    void privateFunction(int x, int y);
    void privateFunctionStatic(int x, int y) static;

    void privateFunctionInline(int x, int y) {
	// do stuff
    };

    public:
    class pubClassAfterFunc {
	int x;
    };

};


void globalFuncDec(int arg1, int arg2) static {
    // Stuff
}


void globalFuncDef(int arg1, int arg2) static {
    // Stuff
}



#endif
