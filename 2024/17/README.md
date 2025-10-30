# 17

While solving this problem I observed following things about my input:

1. the value from "out" instruction only directly depended on value in register
   "A" at the start of the program.

2. There were no "jnz" instruction before "out" instruction.

3. "jnz" instruction took the program to the beginning and not somewhere in the
   middle.

3. There was only one "out" instruction in the program.

4. The value in the "A" register got right shifted by 3 before jumping back to
   beginning.

I am not sure if only my input followed these assumptions and made my life easy 
or its the case with every input. 

My solution is designed for the following assumptions and is not universal. My
solution may not work with other inputs if it breaks any of the assumptions 
stated above.