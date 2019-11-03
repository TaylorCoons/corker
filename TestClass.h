#ifndef TestClass_h
#define TestClass_h

#include <stuff>

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
    struct publicStruct{ 
        int x;
        int y;
    };
    enum enum1 {
        int x;
        int y;
    };
    


};







#endif
