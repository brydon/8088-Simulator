"""
    Copyright (C) 2014 Brydon Eastman

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. Or by
    email to brydon.eastman@gmail.com.
"""

class CommandInterpreter(object):
    _ERROR = -1
    _LABEL = 1
    _INT = 2
    _HEX = 3
    _LOCALVAR = 4
    _REG8 = 5
    _DATA = 6
    _BSS = 7
    _REG = 8
    _MEM = 9
    _IMMED = 10
    _CHAR = 11

    def __init__(self, gui, assembler):
        """ Link's this module with the self.assembler instance """
        self.SYSCodes = {"_EXIT":1, "_PRINTF":127, "_GETCHAR":117, "_SSCANF":125, "_READ":3, "_OPEN":5, "_CLOSE":6}
        self.assembler = assembler
        self.gui = gui
        self.LIST_TYPE = type([1, 1])

    def getCommandArgs(self):
        """ A dict whose keys are commands and their values are the # of arguments they expect """
        return {"AAA":0,  # Ascii adjust AL after ADDition
                "AAD":0,  # Ascii adjust AX before division
                "AAM":0,  # Ascii adjust AX after multiplication
                "AAS":0,  # Ascii adjust AL after subtraction
                "ADC":2,  # Add with carry
                "ADD":2,  # Add
                "AND":2,  # Logical and
                "CALL":1,  # Call procedure
                "CBW":0,  # Convert byte to word
                "CLC":0,  # Clear carry flag
                "CLD":0,  # Clear direction flag
                "CLI":0,  # Clear interrupt flag
                "CMC":0,  # Coplement carry flag
                "CMP":2,  # Compare operands
                "CMPB":2,
                "CMPSB":-1,  # Compare bytes in memory
                "CMPSW":-1,  # Compare words in memory
                "DAA":0,  # Decimal adjust AL after ADDition
                "DAS":0,  # Decimal adjust AL after subtraction
                "DEC":1,  # Decrement by 1
                "DIV":2,  # Unsigned divide
                "IDIV":1,  # Signed divide
                "IMUL":1,  # Signed multiply
                "INC":1,  # Increment by 1
                "JA":1,  # Jump if above
                "JAE":1,  # Jump if above or equal
                "JB":1,  # Jump if below
                "JBE":1,  # Jump if below or equal
                "JC":1,  # Jump if carry
                "JCXZ":1,  # Jump if CX is zero
                "JE":1,  # Jump if equal
                "JG":1,  # Jump if greater than
                "JGE":1,  # Jump if greater than or equal
                "JL":1,  # Jump if less than
                "JLE":1,  # Jump if less than or equal
                "JMP":1,  # Jump
                "JNA":1,  # Jump if not above
                "JNAE":1,  # Jump if not above or equal
                "JNB":1,  # Jump if not below
                "JNBE":1,  # Jump if not below or equal
                "JNC":1,  # Jump if not carry
                "JNE":1,  # Jump if not equal
                "JNG":1,  # Jump if not greater than
                "JNGE":1,  # Jump if not greater than or equal
                "JNL":1,  # Jump if not less than
                "JNLE":1,  # Jump if not less than or equal
                "JNO":1,  # Jump if not overflow
                "JNP":1,  # Jump if not ???
                "JNS":1,  # Jump if not ???
                "JNZ":1,  # Jump if noscreet zero
                "JO":1,  # Jump if overflow
                "JP":1,  # Jump if ???
                "JPE":1,  # Jump if ???
                "JPO":1,  # Jump if ???
                "JS":1,  # Jump if ???
                "JZ":1,  # Jump if zero
                "LAHF":0,  # Load flags into AH register
                "LDS":2,  # Load pointer using DS
                "LEA":2,  # Load effective address
                "LES":2,  # Load ES with pointer
                "LODSB":0,  # Load string byte
                "LODSW":0,  # Load string word
                "LOOP":1,  # Loop control
                "LOOPE":1,  # Loop if equal
                "LOOPNE":1,  # Loop if not equal
                "LOOPNZ":1,  # Loop if not zero
                "LOOPZ":1,  # Loop if zero
                "MOV":2,  # Move
                "MOVSB":0,  # Move byte from string to string
                "MOVSW":0,  # Move word from string to string
                "MUL":2,  # Unsigned Multiply
                "NEG":1,  # Two's complement NEGation
                "NOP":0,  # No Operation.
                "NOT":1,  # Negate the opearand, logical NOT
                "OR":2,  # Logical OR
                "POP":1,  # Pop data from stack
                "POPF":0,  # Pop data from flags register
                "PUSH":1,  # Push data to stacscreek
                "PUSHF":0,  # Push flags onto stack
                "RCL":2,  # Rotate left with carry
                "RCR":2,  # Rotate right with carry
                "REP":-1,  # Repeat MOVS/STOS/CMPS/LODS/SCAS
                "REPE":-1,  # Repeat if equal
                "REPNE":-1,  # Repeat if not equal
                "REPNZ":-1,  # Repeat if not zero
                "REPZ":-1,  # Repeat if zero
                "RET":0,  # Return from procedure
                "ROL":2,  # Rotate left
                "ROR":2,  # Rotate right
                "SAHF":0,  # Store AH into flags
                "SAL":2,  # Shift Arithmetically Left
                "SAR":2,  # Shift Arithmetically Right
                "SBB":2,  # Subtraction with borrow
                "SCASB":0,  # Compare byte string
                "SCASW":0,  # Compare word string
                "SHL":2,  # unsigned Shift left
                "SHR":2,  # unsigned Shift right
                "STC":0,  # Set carry flag
                "STD":0,  # Set direction flag
                "STI":0,  # Set interrupt flag
                "STOSB":0,  # Store byte in string
                "STOSW":0,  # Store word in string
                "SUB":2,  # Subtraction
                "SYS":0,  # System trap
                "TEST":2,  # Logical compare (AND)
                "XCHG":2,  # Exchange data
                "XOR":2  # Logical XOR
                }

    def getFunctionTable(self):
        """ The jump table - the keys are commands and values are the functions that need called, i use anonymous lambda fnxns for argument passing """
        """
                "JNA":1,  # Jump if not above
                "JNAE":1,  # Jump if not above or equal
                "JNB":1,  # Jump if not below
                "JNBE":1,  # Jump if not below or equal
                """
        return {
                "AAA":self.AAA,
                "AAD":self.AAD,
                "AAM":self.AAM,
                "AAS":self.AAS,
                "ADC":self.ADC,
                "ADD":self.ADD,
                "AND":self.AND,
                "CALL":self.CALL,
                "CLC":self.CLC,
                "CLD":self.CLD,
                "CLI":self.CLI,
                "CMPB":self.CMPB,
                "DAA":self.DAA,
                "DAS":self.DAS,
                "DEC":self.DEC,
                "INC":self.INC,
                "JA":self.JA,
                "JAE":self.JAE,
                "JB":self.JB,
                "JBE":self.JBE,
                "JC":self.JC,
                "JCXZ":self.JCXZ,
                "JE":self.JE,
                "JG":self.JG,
                "JGE":self.JGE,
                "JL":self.JL,
                "JLE":self.JLE,
                "JMP":self.JMP,
                "JNA":self.JNA,
                "JNAE":self.JNAE,
                "JNB":self.JNB,
                "JNBE":self.JNBE,
                "JNC":self.JNC,
                "JNE":self.JNE,
                "JNG":self.JNG,
                "JNGE":self.JNGE,
                "JNL":self.JNL,
                "JNLE":self.JNLE,
                "JNO":self.JNO,
                "JNP":self.JNP,
                "JNS":self.JNS,
                "JNZ":self.JNZ,
                "JO":self.JO,
                "JP":self.JP,
                "JPE":self.JPE,
                "JPO":self.JPO,
                "JS":self.JS,
                "JZ":self.JZ,
                "LODSB":self.LODSB,
                "LODSW":self.LODSW,
                "LOOP":self.LOOP,
                "LOOPE":self.LOOPE,
                "LOOPNE":self.LOOPNE,
                "LOOPNZ":self.LOOPNZ,
                "LOOPZ":self.LOOPZ,
                "MOV":self.MOV,
                "NOP":self.NOP,  # best instruction
                "NOT":self.NOT,
                "OR":self.OR,
                "POP":self.POP,
                "POPF":self.POPF,
                "PUSH":self.PUSH,
                "PUSHF":self.PUSHF,
                "RCL":self.RCL,
                "RCR":self.RCR,
                "REP":self.REP,
                "REPE":self.REPE,
                "REPNE":self.REPNE,
                "REPNZ":self.REPNZ,
                "REPZ":self.REPZ,
                "RET":self.RET,
                "ROL":self.ROL,
                "ROR":self.ROR,
                "SAL":self.SAL,
                "SAR":self.SAR,
                "SBB":self.SBB,
                "SHL":self.SHL,
                "SHR":self.SHR,
                "STC":self.STC,
                "STD":self.STD,
                "STI":self.STI,
                "STOSB":self.STOSB,
                "STOSW":self.STOSW,
                "SUB":self.SUB,
                "SYS":self.SYS,
                "XCHG":self.XCHG,
                "XOR":self.XOR
                }

    def AAA(self, command, i):
        """name:AAA
        title:ASCII Adjust AL After Addition
        args:None
        description:Adjusts the result in AL after two ASCII digits have been added together. If AL>9, the high digit of the result is placed in AH, and the Carry and Auxiliary flags are set.
        flags:?,,,?,?,*,?,*"""
        if (self.assembler.getEightBitRegister('AL') & 15 > 9) or self.assembler.getFlag('A'):
            tempAH = self.assembler.getEightBitRegister('AH')
            self.assembler.setRegister('AX', (self.assembler.getEightBitRegister('AL') + 6) & 15)
            self.assembler.setRegister('AX', self.assembler.getREgister('AX') + (tempAH + 1) * 256)
            self.assembler.setFlag('A')
            self.assembler.setFlag('C')
        else:
            self.assembler.setFlag('A', 0)
            self.assembler.setFlag('C', 0)

    def AAD(self, command, i):
        """name:AAD
        title:ASCII Adjust AL Before Division
        args:None
        description:Converts unpacked BCD digits in AH and AL to a single binary value in preperation for the DIV instruction.
        flags:?,,,*,*,?,*,?"""
        self.assembler.setRegister('AX', self.assembler.getEightBitRegister('AL') + self.assembler.getEightBitRegister('AH') * 10)

    def AAM(self, command, i):
        """name:AAM
        title:ASCII Adjust AL After Multiplication
        args:None
        description:Adjusts the result in AX after two unpacked BCD digits have been multiplied together
        flags:?,,,*,*,?,*,?"""
        tempAL = self.assembler.getEightBitRegister('AL')
        self.assembler.setRegister('AX', (tempAL % 10) + (tempAL / 10) * 256)

    def AAS(self, command, i):
        """name:AAS
        title:ASCII Adjust AL After Subtraction
        args:None
        description:Adjusts the result in AX after a subtraction operation. If AL>9, AAS decrements AH and sets the Carry and Auxiliary Carry flags.
        flags:?,,,?,?,*,?,*"""
        if (self.assembler.getEightBitRegister('AL') & 15 > 9) or self.assembler.getFlag('A'):
            tempAH = self.assembler.getEightBitRegister('AH')
            self.assembler.setRegister('AX', (self.assembler.getEightBitRegister('AL') - 6) & 15)
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') + (tempAH - 1) * 256)
            self.assembler.setFlag('A')
            self.assembler.setFlag('C')
        else:
            self.assembler.setFlag('A', 0)
            self.assembler.setFlag('C', 0)

    def ADC(self, command, i):
        """name:ADC
        title:Add with Carry
        args:[reg:mem],[reg:mem:immed]
        description:Adds the source and destination operands, and adds the contents of the Carry flag to the sum, which is stored in the destination
        flags:*,,,*,*,*,*,*"""
        self.ADD(command, i, carry=True)

    def ADD(self, command, i, carry=False, inPlace=False):
        """name:ADD
        title:Add
        args:[reg:mem],[reg:mem:immed]
        description:A source operand is added to a destination operand, and the sum is stored in the destination.
        flags:*,,,*,*,*,*,*"""

        if command[1] == "SP" and command[2].isdigit():
            for j in range(int(command[2]) / 2):
                if len(self.assembler.getStack()) > 0:
                    self.assembler.getStack().pop()
                    self.gui.updateStack()
            self.assembler.setRegister('SP', self.assembler.getRegister('SP') + int(command[2]))
            return

        if self.assembler.isHex(command[1]):
            if not inPlace:
                self.gui.outPut("Error on line " + str(i) + ". " + command[0] + " cannot have a numerical first argument.")
                self.gui.stopRunning(-1)
                return

        argumentType = self.testArgument(command, 2, i, [self._REG, self._MEM, self._IMMED])
        y = self.getValue(command[2], argumentType)

        if carry: y += self.assembler.getFlag('C')
        if command[0].upper() in ["SUB", "SBB", "CMP", "CMPB", "SCASB", "SCASW"]: y *= -1

        if not inPlace:
            argumentType = self.testArgument(command, 1, i, [self._REG, self._MEM])
            result = self.getValue(command[1], argumentType) + y
        else:
            result = int(command[1], 10) + y


        self.assembler.setFlag('O', 0)
        if result >= 2 ** 15:
            while result >= 2 ** 15:
                result -= 2 ** 16
            self.assembler.setFlag('O')
        elif result < -2 ** 15:
            while result < -2 ** 15:
                result += 2 ** 16
            self.assembler.setFlag('O')

        if not inPlace:
            self.setValue(command[1], argumentType, result)

        self.assembler.setFlag('Z', result == 0)
        self.assembler.setFlag('S', result < 0)
        self.assembler.setFlag('P', result % 2)

    def AND(self, command, i, inPlace=False):
        """name:AND
        title:Logical And
        args:[reg:mem],[reg:mem:immed]
        description:Each bit in the destination operand is ANDed with the corresponding bit in the source operand
        flags:*,,,*,*,?,*,0"""

        argumentType = self.testArgument(command, 2, i, (self._IMMED, self._REG, self._MEM))
        t = self.getValue(command[2], argumentType)

        argumentType = self.testArgument(command, 1, i, (self._REG, self._MEM))
        result = self.getValue(command[1], argumentType) & t
        self.setValue(command[1], argumentType, result)

        self.assembler.setFlag('P', result % 2)
        self.assembler.setFlag('S', result < 0)
        self.assembler.setFlag('Z', result == 0)
        self.assembler.setFlag('C', 0)

    def CALL(self, command, i):
        """name:CALL
        title:Call
        args:[label]
        description:Calls the function in the source operand. The current program counter value is pushed to the stack before the call.
        flags:,,,,,,,
        """
        if command[1] in self.assembler.getLookupTable().keys():
            self.assembler.setJumpLocation(self.assembler.getLookupTable()[command[1]])
            self.assembler.getStack().append(self.assembler.getRegister('PC') + 1)
            self.gui.updateStack()
        else:
            self.gui.outPut("Error on line " + str(i) + ". Cannot CALL the label " + command[1] + ". It does not exist.")
            self.gui.stopRunning(-1)

    def CBW(self, command, i):
        """name:CBW
        title:Convert Byte to Word
        args:None
        description:Extends the sign bit in AL throughout the AH register
        flags:,,,,,,,"""
        if self.assembler.getEightBitRegister("AL") >= 128:
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') - 256)

    def CLC(self, command, i):
        """name:CLC
        title:Clear carry flag
        args:None
        description:Clears the carry flag to zero.
        flags:,,,,,,,0
        """
        self.assembler.setFlag("C", 0)

    def CLD(self, command, i):
        """name:CLD
        title:Clear direction flag
        args:None
        description:Clears the Direction flag to zero. String primitive instructions will automatically increment SI and DI
        flags:,0,,,,,,"""
        self.assembler.setFlag("D", 0)

    def CLI(self, commmand, i):
        """name:CLI
        title:Clear Interrupt flag
        args:None
        description:Clears the interrupt flag to zero. This disables maskable hardware interrupts until an STI instruction is executed
        flags:,,0,,,,,"""
        self.assembler.setFlag("I", 0)

    def CMC(self, command, i):
        """name:CMC
        title:Complement Carry flag
        args:None
        description:Toggles the current value of the Carry flag
        flags:,,,,,,,*"""
        self.assembler.setFlag("C", not self.assembler.getFlag('C'))

    def CMPB(self, command, i):
        """name:CMPB
        title:Compare Byte
        args:[reg8:mem],[reg8:mem:immed]
        description:Compares the destination byte to the source byte by performing an implied subtraction of the source from the destination.
        flags:*,,,*,*,*,*,*"""
        a = command[1:3]
        b = []
        for x in a:
            if x in ['AH', 'AL', 'BH', 'BL', 'CH', 'CL', 'DH', 'DL']:
                x = self.assembler.getEightBitRegister(x)
            elif x in ['AX', 'BX', 'CX', 'DX']:
                self.gui.outPut("Illegal argument for CMPB on line %d. %s is a 16 bit register, perhaps you meant one of the 8 bit %s or %s registers?" % (i, x, x[0] + "H", x[0] + "L"))
                self.gui.stopRunning(-1)
                return
            elif type(x) == type(""):
                x = self.assembler.replaceEscapedSequences(x.rstrip("'\"").lstrip("'\""))

                if len(x) != 1:
                    self.gui.outPut("Illegal argument %s for CMPB on line %d. CMPB expects all strings to be ONE byte in length." % (x, i))
                    self.gui.stopRunning(-1)
                    return
                else:
                    try:
                        x = int(x, 16) % 255
                    except ValueError:
                        x = ord(x)
            elif type(x) != type(1):
                self.gui.outPut("Illegal argument %s for CMPB on line %d. CMPB expects an argument to be a one byte register (ie: AH, AL, etc.), an integer, or a one byte string (ie: \"L\", etc.). Instead %s was given." % (x, i, x))
                self.gui.stopRunning(-1)
            b.append(x)

        self.SUB(["CMPB", str(b[0]), str(b[1])], i, inPlace=True)

    def DAA(self, command, i):
        """name:DAA
        title:Decimal adjust after addition
        args:None
        description:Adjusts the binary sum in AL after two packed BCD values have been added. Converts the sum to two BCD digits in AL.
        flags:?,,,*,*,*,*,*"""

        if (self.assembler.getEightBitRegister('AL') & 15 > 9) or self.assembler.getFlag('A'):
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') + 6)
            self.assembler.setFlag('A')
        else:
            self.assembler.setFlag('A', 0)

        if self.assembler.getEightBitRegister('AL') > 159 or self.assembler.getFlag('C'):
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') + 96)
            self.assembler.setFlag('C')
        else:
            self.assembler.setFlag('C', 0)

    def DAS(self, command, i):
        """name:DAS
        title:Decimal adjust after subtraction
        args:None
        description:Converts the binary result of a subtraction operation to two packed BCD digits in AL.
        flags:?,,,*,*,*,*,*"""

        if (self.assembler.getEightBitRegister('AL') & 15 > 9) or self.assembler.getFlag('A'):
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') - 6)
            self.assembler.setFlag('A')
        else:
            self.assembler.setFlag('A', 0)

        if self.assembler.getEightBitRegister('AL') > 159 or self.assembler.getFlag('C'):
            self.assembler.setRegister('AX', self.assembler.getRegister('AX') - 96)
            self.assembler.setFlag('C')
        else:
            self.assembler.setFlag('C', 0)

    def DEC(self, command, i):
        """name:DEC
        title:Decrement
        args: [reg:mem]
        description:Subtracts one from the register or memory address provided 
        flags:*,,,*,*,*,*,"""
        self.incdec(command, i, -1)

    def INC(self, command, i):
        """name:INC
        title:Increment
        args: [reg:mem]
        description:Adds one to the register or memory address provided 
        flags:*,,,*,*,*,*,"""
        self.incdec(command, i, 1)

    def JA(self, command, i):
        """name:JA
        title:Jump to a label if above
        args: [label]
        description:The same as JG. Jumps if the sign flag is clear and the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(self, i, not self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JAE(self, command, i):
        """name:JAE
        title:Jump to a label if above or equal
        args: [label]
        description:The same as JGE. Jumps if the sign flag is clear and/or the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JB(self, command, i):
        """name:JB
        title:Jump to a label if below
        args: [label]
        description:The same as JL. Jumps if the sign flag is set and the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JBE(self, command, i):
        """name:JBE
        title:Jump to a label if below or equal
        args: [label]
        description:The same as JLE. Jumps if the sign flag is set and/or the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JC(self, command, i):
        """name:JC
        title:Jump to a label if carry
        args: [label]
        description:Jumps if the carry flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('C'))

    def JCXZ(self, command, i):
        """name:JCXZ
        title:Jump to a label if CX is zero
        args: [label]
        description:Jumps if the value of the CX register is zero 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getRegister('CX') == 0)

    def JE(self, command, i):
        """name:JE
        title:Jump to a label if equal
        args: [label]
        description:Jumps if the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('Z'))

    def JG(self, command, i):
        """name:JG
        title:Jump to a label if greater than
        args: [label]
        description:Jumps if the sign flag is clear and the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JGE(self, command, i):
        """name:JGE
        title:Jump to a label if greater than or equal
        args: [label]
        description:Jumps if the sign flag is clear and/or the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JL(self, command, i):
        """name:JL
        title:Jump to a label if less than
        args: [label]
        description:Jumps if the sign flag is set and the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JLE(self, command, i):
        """name:JLE
        title:Jump to a label if less than or equal
        args: [label]
        description:Jumps if the sign flag is set and/or the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JNA(self, command, i):
        """name:JNA
        title:Jump to a label if not above
        args: [label]
        description:The same as JLE. Jumps if the sign flag is set and/or the zero flag is set. 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JNAE(self, command, i):
        """name:JNAE
        title:Jump to a label if not above or equal
        args: [label]
        description:The same as JL. Jumps if the sign flag is set and the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JNB(self, command, i):
        """name:JNB
        title:Jump to a label if not below
        args: [label]
        description:The same as JGE. Jumps if the sign flag is clear and/or the zero flag is set.
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JNBE(self, command, i):
        """name:JNBE
        title:Jump to a label if not below or equal
        args: [label]
        description:The same as JG. Jumps if the sign flag is clear and the zero flag is clear. 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JNC(self, command, i):
        """name:JNC
        title:Jump to a label if not carry
        args: [label]
        description:Jumps if the carry flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('C'))

    def JNE(self, command, i):
        """name:JNE
        title:Jump to a label if not equal
        args: [label]
        description:Jumps if the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('Z'))

    def JNG(self, command, i):
        """name:JNG
        title:Jump to a label if not greater than
        args: [label]
        description:The same as JLE. Jumps if the sign flag is set and/or the zero flag is set. 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JNGE(self, command, i):
        """name:JNGE
        title:Jump to a label if not greater than or equal
        args: [label]
        description:The same as JL. Jumps if the sign flag is set and the zero flag is clear. 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JNL(self, command, i):
        """name:JNL
        title:Jump to a label if not less than
        args: [label]
        description:The same as JGE. Jumps if the sign flag is clear and/or the zero flag is set. 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') or self.assembler.getFlag('Z'))

    def JNLE(self, command, i):
        """name:JNLE
        title:Jump to a label if not less than or equal
        args: [label]
        description:The same as JG. Jumps if the sign flag is clear and the zero flag is clear. 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S') and not self.assembler.getFlag('Z'))

    def JNO(self, command, i):
        """name:JNO
        title:Jump to a label if not overflow
        args: [label]
        description:Jumps if the overflow flag is clear. 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('O'))

    def JNP(self, command, i):
        """name:JNP
        title:Jump to a label if not parity
        args: [label]
        description:Jumps if the parity flag is clear.  
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('P'))

    def JNS(self, command, i):
        """name:JC
        title:Jump to a label if not sign.
        args: [label]
        description:The same as JG. Jumps if the sign flag is clear.
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('S'))

    def JNZ(self, command, i):
        """name:JC
        title:Jump to a label if not zero
        args: [label]
        description:Jumps if the zero flag is clear 
        flags:,,,,,,,"""
        self.jf(command, i, not self.assembler.getFlag('Z'))

    def JO(self, command, i):
        """name:JC
        title:Jump to a label if overflow.
        args: [label]
        description:Jumps if the overflow flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('O'))

    def JP(self, command, i):
        """name:JC
        title:Jump to a label if parity
        args: [label]
        description:Jumps if the parity flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('P'))

    def JPE(self, command, i):
        """name:JC
        title:Jump to a label if parity or equal
        args: [label]
        description:Jumps if the parity flag is set and/or the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('P') or self.assembler.getFlag('Z'))

    def JPO(self, command, i):
        """name:JC
        title:Jump to a label if parity or overflow
        args: [label]
        description:Jumps if the parity flag is set or the overflow flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('P') or self.assembler.getFlag('O'))

    def JS(self, command, i):
        """name:JC
        title:Jump to a label if sign
        args: [label]
        description:The same as JL. Jumps if the sign flag is set. 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('S'))

    def JZ(self, command, i):
        """name:JC
        title:Jump to a label if zero
        args: [label]
        description:The same as JE. Jumps if the zero flag is set 
        flags:,,,,,,,"""
        self.jf(command, i, self.assembler.getFlag('Z'))

    def JMP(self, command, i, referer="JMP"):
        """name:JMP
        title:Jump unconditionally to a label
        args: [label]
        description:The program counter is adjusted to the value referenced by the label and program execution continues.
        flags:,,,,,,,"""
        if command[1] in self.assembler.getLookupTable().keys() and not self.assembler.isHex(command[1]):
            self.assembler.setJumpLocation(self.assembler.getLookupTable()[command[1]])
        elif (command[1].rstrip('b').isdigit() or command[1].rstrip('f').isdigit()) and command[1].strip('bf') in self.assembler.getLookupTable().keys():
            temp = command[1].rstrip('bf')
            m = -1
            if type(self.assembler.getLookupTable()[temp]) == self.LIST_TYPE:
                for x in self.assembler.getLookupTable()[temp]:
                    if command[1][-1] == 'b':
                        if x < self.assembler.getRegister('PC') and (m < x or m == -1):
                            m = x
                    else:
                        if x > self.assembler.getRegister('PC') and (x < m or m == -1):
                            m = x
            else:
                m = self.assembler.getLookupTable()[temp]

            if m == -1:
                self.gui.outPut("Fatal error on line " + str(i) + ". The label " + command[1] + " could not be resolved.")
                self.gui.stopRunning(-1)
            else:
                self.assembler.setJumpLocation(m)

        elif self.assembler.isHex(command[1]):
            if command[1][-1] == "h":
                self.assembler.setJumpLocation(int(command[1][:-1], 16))
            else:
                self.assembler.setJumpLocation(int(command[1]))
        else:
            self.gui.outPut("Error on line " + str(i) + ". The label " + command[1] + " is not defined for " + referer + "-ing to.")

    def LODSB(self, command, i):
        """name:LODSB
        title:Load accumulator from string
        args: None
        description: Loads a memory byte addressed by SI into AL.
        flags:,,,,,,,"""
        self.assembler.setRegister('AX', self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI')))

        self.assembler.setRegister('SI', self.assembler.getRegister('SI') - 1 if self.assembler.getFlag('D') else self.assembler.getRegister('SI') + 1)

    def LODSW(self, command, i):
        """name:LODSW
        title:Load accumulator from string
        args:None
        description:Loads a memory word addressed by SI into AX.
        flags:,,,,,,,"""
        self.assembler.setRegister('AX', self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI')) + self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI') + 1) * 256)

        self.assembler.setRegister('SI', self.assembler.getRegister('SI') - 2 if self.assembler.getFlag('D') else self.assembler.getRegister('SI') + 2)

    def LOOP(self, command, i, flag=True):
        """name:LOOP
        title: Loop
        args: [label]
        description: Decrements CX and jumps to the label if CX is greater than zero.
        flags:,,,,,,,"""

        self.testArgument(command, 1, i, [self._LABEL])

        if flag and self.assembler.getRegister("CX") > 0:
            self.JMP(command, i, "LOOP")
            self.assembler.setRegister("CX", self.assembler.getRegister('CX') - 1)

    def LOOPE(self, command, i):
        """name:LOOPE
        title:Loop if equal
        args:[label]
        description:Decrements CX and jumps to a label if CX>0 and the Zero flag is set.
        flags:,,,,,,,"""
        self.LOOP(command, i, self.assembler.getFlag('Z'))

    def LOOPNE(self, command, i):
        """name:LOOPNE
        title:Loop if not equal
        args:[label]
        description:Decrements CX and jumps to a label if CX>0 and the Zero flag is clear.
        flags:,,,,,,,"""
        self.LOOP(command, i, not self.assembler.getFlag('Z'))

    def LOOPNZ(self, command, i):
        """name:LOOPNZ
        title:Loop if not zero
        args:[label]
        description:Decrements CX and jumps to a label if CX>0 and the Zero flag is clear.
        flags:,,,,,,,"""
        self.LOOP(command, i, not self.assembler.getFlag('Z'))

    def LOOPZ(self, command, i):
        """name:LOOPZ
        title:Loop if zero
        args:[label]
        description:Decrements CX and jumps to a label if CX>0 and the Zero flag is set.
        flags:,,,,,,,"""
        self.LOOP(command, i, self.assembler.getFlag('Z'))

    def MOV(self, command, i):
        """name:MOV
        title:Move
        args:[reg:mem],[reg:mem:immed]
        description:Copies a byte or word from a source operand to a destination operand.
        flags:,,,,,,,"""

        argumentType = self.testArgument(command, 2, i, (self._IMMED, self._REG, self._MEM))
        t = self.getValue(command[2], argumentType)

        argumentType = self.testArgument(command, 1, i, (self._REG, self._MEM))

        self.setValue(command[1], argumentType, t)

    def NOP(self, command, i):
        """name:NOP
        title:No Operation
        args:None
        description:Does nothing. Usually implemented at machine level as XCHG AX,AX
        flags:,,,,,,,"""
        return

    def MOVSB(self, command, i):
        """name:MOVSB
        title:Move string
        args:None
        description:Copies a byte from memory addressed by SI to a memory addressed by DI. SI and DI are increased if the Direction flag is clear (0) and decreased if the Direction flag is set (1).
        flags:,,,,,,,"""
        self.assembler.setMemoryAddress(self.assembler.getRegister('DI'), self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI')))
        self.assembler.setRegister('SI', self.assembler.getRegister('SI') - 1 if self.assembler.getFlag('D') else self.assembler.getRegister('SI') + 1)


    def MOVSW(self, command, i):
        """name:MOVSW
        title:Move string
        args:None
        description:Copies a word from memory addressed by SI to a memory addressed by DI. SI and DI are increased if the Direction flag is clear (0) and decreased if the Direction flag is set (1).
        flags:,,,,,,,"""
        self.assembler.setMemoryAddress(self.assembler.getRegister('DI'), self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI')))
        self.assembler.setMemoryAddress(self.assembler.getRegister('DI') + 1, self.assembler.getFromMemoryAddress(self.assembler.getRegister('SI') + 1))
        self.assembler.setRegister('SI', self.assembler.getRegister('SI') - 2 if self.assembler.getFlag('D') else self.assembler.getRegister('SI') + 2)

    def NEG(self, command, i):
        """name:NEG
        title:Negate
        args:[reg]
        description:Calculates the twos complement of the argument in place.
        flags:*,,,*,*,*,*,*"""
        self.testArgument(command, 1, i, [self._REG])

        result = -self.assembler.getRegister(command[1])
        self.assembler.setRegister(command[1], result)

        # TODO: OVERFLOW AND CARRY?

        self.assembler.setFlag('P', result % 2)
        self.assembler.setFlag('S', result < 0)
        self.assembler.setFlag('Z', result == 0)

    def NOT(self, command, i):
        """name:NOT
        title:Logical Not
        args:[reg:mem]
        description:Performs a logical not on an operand by reversing each of its bits.
        flags:,,,,,,,"""
        argType = self.testArgument(command, 1, i, [self._REG, self._MEM])
        self.setValue(command[1], argType, ~self.getValue(command[1], argType))

    def OR(self, command, i):
        """name:OR
        title:Inclusive Or
        args:[reg:mem],[reg:mem:immed]
        description:Performs a logical OR between each bit in the destination operand and each bit in the source operand. If either bit is a 1 in each position, the result bit is a 1.
        flags:0,,,*,*,?,*,0"""

        argumentType = self.testArgument(command, 2, i, (self._IMMED, self._REG, self._MEM))
        t = self.getValue(command[2], argumentType)

        argumentType = self.testArgument(command, 1, i, (self._REG, self._MEM))
        result = self.getValue(command[1], argumentType) | t
        self.setValue(command[1], argumentType, result)

        self.assembler.setFlag('P', result % 2)
        self.assembler.setFlag('S', result < 0)
        self.assembler.setFlag('Z', result == 0)
        self.assembler.setFlag('O', 0)
        self.assembler.setFlag('C', 0)

    def POP(self, command, i):
        """name:POP
        title:Pop from stack
        args:[reg]
        description:Copies a word at the current stack pointer location into the destination operand, and adds 2 to the SP.
        flags:,,,,,,,"""
        self.testArgument(command, 1, i, [self._REG])

        self.assembler.setRegister(command[1], int(self.assembler.getStack().pop()))
        self.assembler.setRegister('SP', self.assembler.getRegister('SP') + 2)
        self.gui.updateStack()

    def POPF(self, command, i):
        """name:POPF
        title:Pop flags from stack
        args:None
        description:POPF pops the top of the stack into the 16-bit Flags register.
        flags:*,*,*,*,*,*,*,*"""
        flags = self.assembler.getStack().pop()

        self.assembler.setFlag('C', flags % 2)
        flags /= 4
        self.assembler.setFlag('P', flags % 2)
        flags /= 4
        self.assembler.setFlag('A', flags % 2)
        flags /= 4
        self.assembler.setFlag('Z', flags % 2)
        flags /= 2
        self.assembler.setFlag('S', flags % 2)

        self.gui.updateStack()
        self.assembler.setRegister('SP', self.assembler.getRegister('SP') + 2)

    def PUSH(self, command, i):
        """name:PUSH
        title:Push on stack
        args:[reg:mem:immed]
        description:Subtracts 2 from SP and copies the source operand into the stack location pointed to by SP.
        flags:,,,,,,,"""
        argType = self.testArgument(command, 1, i, [self._REG, self._MEM, self._IMMED])

        self.assembler.getStack().append(self.getValue(command[1], argType))

        """if "(" in command[1] and ")" in command[1]:
            temp = command[1][command[1].find("(") + 1:command[1].find(")")]
            if temp in self.assembler.getBSS().keys():
                # TODO: memory
                1 + 1
            else:
                self.gui.outPut("Error on line " + str(i) + ". I don't understand what (" + temp + ") is")
                self.gui.stopRunning(-1)"""

        self.assembler.setRegister('SP', self.assembler.getRegister('SP') - 2)
        self.gui.updateStack()

    def PUSHF(self, command, i):
        """name:PUSHF
        title:Push flags onto the stack
        args:None
        description:PUSHF pushes the Flags register onto the stack.
        flags:,,,,,,,"""
        flags = self.assembler.getFlag('S') * (128) + self.assembler.getFlag('Z') * (64) + self.assembler.getFlag('A') * (16) + self.assembler.getFlag('P') * (4) + self.assembler.getFlag('C')
        self.assembler.getStack().append(flags)
        self.assembler.setRegister('SP', self.assembler.getRegister('SP') - 2)
        self.gui.updateStack()

    def RCL(self, command, i):
        """name:RCL
        title:Rotate carry left
        args:[reg]
        description:Rotates the destionation operand left. The carry flag is copied into the lowest bit, and the highest bit is copied into the Carry flag
        flags:*,,,,,,,*"""
        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg < 0

        if temp:
            reg += 2 ** 16

        reg = reg << 1
        reg += self.assembler.getFlag('C')

        while reg >= 2 ** 15:
            reg -= 2 ** 16

        self.assembler.setRegister(command[1], reg)

        self.assembler.setFlag('C', temp)

    def RCR(self, command, i):
        """name:RCR
        title:Rotates carry right
        args:[reg]
        description:Rotates the destination operand right, using the source operand to determine the number of rotations. The carry flag is copied into the highest bit, and the lowest bit is copied into the Carry flag.
        flags:*,,,,,,,*"""
        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])

        temp = reg % 2

        if reg < 0:
            reg += 2 ** 16

        reg = reg >> 1

        while reg >= 2 ** 15:
            reg -= 2 ** 16

        if self.assembler.getFlag('C'):
            reg -= 2 ** 15

        self.assembler.setRegister(command[1], reg)

        self.assembler.setFlag('C', temp)

    def REP(self, command, i):
        """name:REP
        title:Repeating string primitive command
        args: [MOVS:MOVSB:CMPS:CMPSB:CMPSW:SCAS:SCASB:SCASW:STOS:STOSB:STOSW:LODS:LODSB:LODSW]
        description:Repeats a string primitive instruction, using CX as a counter. CX is decremented each time the instruction is repeated, until CX = 0. EG REP MOVSB
        flags:,,,,,,,"""
        if command[1] in ["MOVS", "MOVSB", "CMPS", "CMPSB", "CMPSW", "SCAS", "SCASB", "SCASW", "STOS", "STOSB", "STOSW", "LODS", "LODSB", "LODSW"]:
            while self.assembler.getRegister('CX') > 0:
                self.getFunctionTable()[command[1:], i]
                self.assembler.setRegister('CX', self.assembler.getRegister('CX') - 1)
        else:
            self.gui.outPut("Innapropriate command used with REP,")
            self.gui.stopRunning(-1)

    def REPE(self, command, i):
        """name:REPE
        title:Repeating string primitive command if equal
        args: [MOVS:MOVSB:CMPS:CMPSB:CMPSW:SCAS:SCASB:SCASW:STOS:STOSB:STOSW:LODS:LODSB:LODSW]
        description:Repeats a string primitive instruction, using CX as a counter. CX is decremented each time the instruction is repeated, until CX = 0 while the zero flag is set. EG REP MOVSB
        flags:,,,,*,,,"""
        if command[1] in ["CMPS", "CMPSB", "CMPSW", "SCAS", "SCASB", "SCASW"]:
            while self.assembler.getFlag("Z") and self.assembler.getRegister('CX') > 0:
                self.getFunctionTable()[command[1:], i]
                self.assembler.setRegister('CX', self.assembler.getRegister('CX') - 1)
        else:
            self.gui.outPut("Innapropriate command used with " + command[0])
            self.gui.stopRunning(-1)

    def REPNE(self, command, i):
        """name:REPNE
        title:Repeating string primitive command if not equal
        args: [MOVS:MOVSB:CMPS:CMPSB:CMPSW:SCAS:SCASB:SCASW:STOS:STOSB:STOSW:LODS:LODSB:LODSW]
        description:Repeats a string primitive instruction, using CX as a counter. CX is decremented each time the instruction is repeated, until CX = 0 while the zero flag is clear. EG REP MOVSB
        flags:,,,,*,,,"""
        if command[1] in ["CMPS", "CMPSB", "CMPSW", "SCAS", "SCASB", "SCASW"]:
            while not self.assembler.getFlag("Z") and self.assembler.getRegister('CX') > 0:
                self.getFunctionTable()[command[1:], i]
                self.assembler.setRegister('CX', self.assembler.getRegister('CX') - 1)
        else:
            self.gui.outPut("Innapropriate command used with " + command[0])
            self.gui.stopRunning(-1)

    def REPNZ(self, command, i):
        """name:REPNZ
        title:Repeating string primitive command if not zero
        args: [MOVS:MOVSB:CMPS:CMPSB:CMPSW:SCAS:SCASB:SCASW:STOS:STOSB:STOSW:LODS:LODSB:LODSW]
        description:Repeats a string primitive instruction, using CX as a counter. CX is decremented each time the instruction is repeated, until CX = 0 while the zero flag is clear. EG REP MOVSB
        flags:,,,,*,,,"""
        self.REPNE(command, i)

    def REPZ(self, command, i):
        """name:REPZ
        title:Repeating string primitive command if zero
        args: [MOVS:MOVSB:CMPS:CMPSB:CMPSW:SCAS:SCASB:SCASW:STOS:STOSB:STOSW:LODS:LODSB:LODSW]
        description:Repeats a string primitive instruction, using CX as a counter. CX is decremented each time the instruction is repeated, until CX = 0 while the zero flag is set. EG REP MOVSB
        flags:,,,,*,,,"""
        self.REPE(command, i)

    def RET(self, command, i):
        """name:RET
        title:Return from procedure
        args:[None:immed]
        description:Pop a return address from the stack. An optional argument tells the CPU to add a value to SP after popping the return address.
        flags:,,,,,,,"""
        if len(self.assembler.getStack()) == 0:
            self.gui.outPut("Fatal Error: The stack is empty and RET was called, there was no address to return to!")
            self.gui.stopRunning(-1)
        elif self.assembler.getCodeBounds()[0] <= self.assembler.getStack()[-1] <= self.assembler.getCodeBounds()[1]:
            self.assembler.setJumpLocation(self.assembler.getStack().pop())
            self.gui.updateStack()
        else:
            self.gui.outPut("Returning on a suspect address.")
            print self.assembler.getCodeBounds()[0]
            print self.assembler.getStack()[-1]
            print self.assembler.getCodeBounds()[1]
            self.gui.stopRunning(-1)

    def ROL(self, command, i):
        """name:ROL
        title:Rotate left
        args:[reg]
        description:Rotates the destination operand left. The highest bit is copied into the Carry flag and moved into the loewst bit position.
        flags:*,,,,,,,*"""
        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg < 0

        if temp:
            reg += 2 ** 16

        reg = reg << 1

        while reg >= 2 ** 15:  # this is when 0100
            reg -= 2 ** 16

        reg += temp

        self.assembler.setRegister(command[1], reg)
        self.assembler.setFlag('C', temp)

    def ROR(self, command, i):
        """name:ROR
        title:Rotate right
        args:[reg]
        description:Rotates the destination operand right. The lowest bit is copied into both the Carry flag and the highest bit position.
        flags:*,,,,,,,*"""
        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg % 2

        while reg < 0:
            reg += 2 ** 16

        reg = reg >> 1

        if reg >= 2 ** 15:
            reg -= 2 ** 16

        reg -= temp * 2 ** 15

        self.assembler.setRegister(command[1], reg)
        self.assembler.setFlag('C', temp)

    def SAHF(self, command, i):
        """name:SAHF
        title:Store AH into flags
        args:None
        description:Copies AH into bits 0 through 7 of the Flags register. The Trap, Interrupt, DIrection, and Overflow flags are not affected.
        flags:,,,*,*,*,*,*"""
        flags = self.assembler.getEightBitRegister('AH')
        for f in ['C', 'P', 'A', 'Z', 'S', 'I', 'D', 'O']:
            self.assembler.setFlags(f, flags % 2)
            flags /= 2
        self.gui.updateStack()

    def SAL(self, command, i):
        """name:SAL
        title:Shift arithmetic left
        args:[reg]
        description:Identical to SHL, only included in the instruction set for completeness.
        flags:*,,,*,*,?,*,*"""
        self.SHL(self, command, i)

    def SAR(self, command, i):
        """name:SAR
        title:Shift arithmetic right
        args:[reg]
        description:Shifts each bit in the destination operand to the right. THe lowest bit is copied into the Carry flag, and the highest bit retains its previous value. This hift is often used with signed operands, because it preserves the number's sign.
        flags:*,,,*,*,?,*,*"""
        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg < 0
        self.assembler.setFlag('C', reg % 2)

        if temp:
            reg += 2 ** 16

        reg = reg >> 1

        while reg >= 2 ** 15:  # this is when 0100
            reg -= 2 ** 16

        reg -= temp * 2 ** 15
        self.assembler.setRegister(command[1], reg)

    def SBB(self, command, i):
        """name:SBB
        title:Subtract with borrow
        args:[reg:mem],[reg:mem:immed]
        description:Subtracts the source operand from the destination operand and then subtracts the Carry flag from the destination.
        flags:*,,,*,*,*,*,*"""

        self.testArgument(command, 1, i, [self._REG, self._MEM])
        self.testArgument(command, 2, i, [self._REG, self._MEM, self._IMMED])

        self.ADD(command, i, carry=True)

    def SCASB(self, command, i):
        """name:SCASB
        title:Scan string
        args:None
        description:Scans a string in memory pointed to by DI for a value that matches AL. DI is increased if the Direction flag is clear (0) and decreased if the Direction flag is set (1).
        flags:*,,,*,*,*,*,*"""
        self.SUB(['SCASB', str(self.assembler.getEightBitRegister('AL')), str(self.assembler.getFromMemoryAddress(self.assembler.getRegister('DI')))], i, inPlace=True)
        self.assembler.setRegister('DI', self.assembler.getRegister('DI') - 1 if self.assembler.getFlag('D') else self.assembler.getRegister('DI') + 1)

    def SCASW(self, command, i):
        """name:SCASW
        title:Scan string
        args:None
        description:Scans a string in memory pointed to by DI for a value that matches AX. DI is increased if the Direction flag is clear (0) and decreased if the Direction flag is set (1).
        flags:,,,,,,,"""
        self.SUB(['SCASW', str(self.assembler.getRegister('AX')), str(self.assembler.getFromMemoryAddress(self.assembler.getRegister('DI') + 1) + 256 * self.assembler.getFromMemoryAddress(self.assembler.getRegister('DI')))], i, inPlace=True)
        self.assembler.setRegister('DI', self.assembler.getRegister('DI') - 2 if self.assembler.getFlag('D') else self.assembler.getRegister('DI') + 2)

    def SHL(self, command, i):
        """name:SHL
        title:Shift left
        args:[reg]
        description:Shifts each bit in the destination operand to the left. The highest bit is copied into the Carry flag and the lowest bit is filled with a zero.
        flags:*,,,*,*,?,*,*"""

        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg < 0

        if temp:
            reg += 2 ** 16

        reg = reg << 1

        if reg >= 2 ** 15:  # this is when 0100
            reg -= 2 ** 16

        self.assembler.setRegister(command[1], reg)
        self.assembler.setFlag('C', temp)

    def SHR(self, command, i):
        """name:SHR
        title:Shift right
        args:None
        description:SHifts each bit in the destination operand to the right. The highest bit is filled with a zero, and the lowest bit is copied into the Carry flag.
        flags:*,,,*,*,?,*,*"""

        self.testArgument(command, 1, i, [self._REG])

        reg = self.assembler.getRegister(command[1])
        temp = reg % 2

        if reg < 0:
            reg += 2 ** 16

        reg = reg >> 1

        if reg >= 2 ** 15:  # this is when 0100
            reg -= 2 ** 16

        self.assembler.setRegister(command[1], reg)
        self.assembler.setFlag('C', temp)

    def STC(self, command, i):
        """name:STC
        title:Set the Carry flag
        args:None
        description:Sets the Carry flag to 1
        flags:,,,,,,,1"""
        self.assembler.setFlag("C")

    def STD(self, command, i):
        """name:STD
        title:Set the Direction flag
        args:None
        description:Sets the Direction flag to 1
        flags:,1,,,,,,"""
        self.assembler.setFlag("D")

    def STI(self, command, i):
        """name:STI
        title:Sets the Interrupt flag
        args:None
        description:Sets the Interrupt flag to 1
        flags:,,1,,,,,"""
        self.assembler.setFlag("I")

    def STOSB(self, command, i):
        """name:STOSB
        title:Store string data
        args:None
        description:Stores the value of AL in the memory location addressed by DI. DI is increased if the Direction flag is clear (0), and decreased if the Direction flag is set (1).
        flags:,,,,,,,"""
        self.assembler.setMemoryAddress(self.assembler.getRegister("DI"), chr(self.assembler.getEightBitRegister("AL")))
        self.assembler.setRegister('DI', self.assembler.getRegister('DI') - 1 if self.assembler.getFlag('D') else self.assembler.getRegister('DI') + 1)

    def STOSW(self, command, i):
        """name:STOSW
        title:Store string data
        args:None
        description:Stores the value of AX in the memory location addressed by DI. DI is increased if the Direction flag is clear (0), and decreased if the Direction flag is set (1).
        flags:,,,,,,,"""
        self.assembler.setMemoryAddress(self.assembler.getRegister("DI"), chr(self.assembler.getEightBitRegister("AH")))
        self.assembler.setMemoryAddress(self.assembler.getRegister("DI") + 1, chr(self.assembler.getEightBitRegister("AL")))
        self.assembler.setRegister('DI', self.assembler.getRegister('DI') - 2 if self.assembler.getFlag('D') else self.assembler.getRegister('DI') + 2)

    def SUB(self, command, i, inPlace=False):
        """name:SUB
        title:Subtract
        args:[reg:mem],[reg:mem:immed]
        description:Subtracts the source opearand from the destination operand.
        flags:*,,,*,*,*,*,*"""
        self.ADD(command, i, inPlace=inPlace)

    def SYS(self, command, i):
        """name:SYS
        title:System trap
        args:None
        description:Calls a system trap: evaluates based on the last piece of data on the stack
        flags:,,,,,,,"""
        if len(self.assembler.getStack()) == 0:
            self.gui.outPut("Invalid system trap: SYS called on line %d without any arguments on stack." % i)
            self.gui.stopRunning(-1)
        elif not int(self.assembler.getStack()[-1]) in self.SYSCodes.values():
            self.gui.outPut("Invalid system trap on line %d: The first argument \"%s\" on the stack is not understood" % (i, self.assembler.getStack()[-1]))
            self.gui.stopRunning(-1)
        else:
            if int(self.assembler.getStack()[-1]) == self.SYSCodes["_EXIT"]:
                self.gui.stopRunning()
            elif int(self.assembler.getStack()[-1]) == self.SYSCodes["_GETCHAR"]:
                self.gui.getChar()
            elif int(self.assembler.getStack()[-1]) == self.SYSCodes["_OPEN"]:
                1 + 1
            elif int(self.assembler.getStack()[-1]) == self.SYSCodes["_PRINTF"]:
                try:
                    i = 2
                    args = []
                    while True:  # TODO: fix this VV
                        if self.assembler.addressSpace.count("0") == 0:
                            formatStr = "".join(self.assembler.addressSpace[int(self.assembler.getStack()[-i]):])
                        else:
                            formatStr = "".join(self.assembler.addressSpace[int(self.assembler.getStack()[-i]):self.assembler.addressSpace.index("0", int(self.assembler.getStack()[-i]))])
                        i += 1
                        print formatStr
                        numArgs = formatStr.count("%") - formatStr.count("\%")
                        if numArgs == len(args): break
                        if numArgs != 0: continue
                        args.append(formatStr)
                    self.gui.outPut(formatStr % tuple(args))
                except IndexError:
                    self.gui.stopRunning(-1)
                    self.gui.outPut("Invalid system trap on line %d. Invalid number of arguments with _PRINTF." % i)

    def TEST(self, command, i):
        """name:TEST
        title:Test
        args:[reg:mem],[reg:mem:immed]
        description:Tests individual bits in the destination operand against those in the source operand. Performs a logial AND operation that affects the flags but not the destination operand.
        flags:0,,,*,*,?,*,0"""
        self.AND(command, i, inPlace=True)

    def XCHG(self, command, i):
        """name:XCHG
        title:Exchange
        args:[reg],[reg]
        description:Exchanges the contents of the source and destination operands
        flags:,,,,,,,"""
        argType1 = self.testArgument(command, 1, i, [self._REG])
        argType2 = self.testArgument(command, 2, i, [self._REG])

        if argType1 == argType2 == self._REG:
            temp = self.assembler.getRegister(command[1])
            self.assembler.setRegister(command[1], self.assembler.getRegister(command[2]))
            self.assembler.setRegister(command[2], temp)

    def XOR(self, command, i):
        """name:XOR
        title:Exclusive OR
        args:[reg:mem],[reg:mem:immed]
        description:Each bit in the source operand is exclusive ORed with its corresponding bit in the destination. The destination bit is a 1 only when the original source and destination bits are different.
        flags:0,,,*,*,?,*,0
        flags:ODISZAPC"""

        argumentType = self.testArgument(command, 2, i, (self._IMMED, self._REG, self._MEM))
        t = self.getValue(command[2], argumentType)

        argumentType = self.testArgument(command, 1, i, (self._REG, self._MEM))
        result = self.getValue(command[1], argumentType) ^ t
        self.setValue(command[1], argumentType, result)

        self.assembler.setFlag('Z', result == 0)
        self.assembler.setFlag('S', result < 0)
        self.assembler.setFlag('P', result % 2)
        self.assembler.setFlag('O', 0)
        self.assembler.setFlag('C', 0)

    def incdec(self, command, i, p):
        """ A function for incrementing or decermenting a register.  p is the polarity (-1 for dec, 1 for inc) """
        argumentType = self.testArgument(command, 1, i, (self._REG, self._MEM))
        result = self.getValue(command[1], argumentType) + p

        self.setValue(command[1], argumentType, result)

    def jf(self, command, i, flag):
        """ JMP if the flag is true, used for jo, jg, jge, etc. """
        if flag:
            self.JMP(command, i)

    def testArgument(self, command, numArg, i, argList, automaticErrors=True):
        """ Tests the arguments to ensure they are legal. 
        Where command is the argument to test and argList is a tuple of legal argument types.
        Returns a constant detailing the argument type found. Or the _ERROR constant if the argument doesnt match."""

        if self._REG in argList:
            if command[numArg] in self.assembler.getRegisterNames():
                return self._REG
        if self._MEM in argList:
            if command[numArg] in self.assembler.getBSS().keys():
                return self._BSS
            elif command[numArg] in self.assembler.getDATA().keys():
                return self._DATA
        if self._REG8 in argList:
            if command[numArg] in self.assembler.getEightBitRegisterNames():
                return self._REG8
        if self._IMMED in argList:
            if self.assembler.isLocalVar(command[numArg]):
                return self._LOCALVAR
            elif self.assembler.isHex(command[numArg]):
                if command[numArg][-1] == "h":
                    return self._HEX
                else:
                    return self._INT
            elif len(command[numArg]) == 3 and len(command[numArg].strip("'").strip('"')) == 1:
                return self._CHAR
        if self._LABEL in argList:
            if command[numArg] in self.assembler.getLookupTable():
                return self._LABEL

        if automaticErrors: self.wrongArgsError(command, i, argList, numArg)
        return self._ERROR

    def getValue(self, arg, argumentType):
        if argumentType == self._REG8:
            return self.assembler.getEightBitRegister(arg)
        elif argumentType == self._REG:
            return self.assembler.getRegister(arg)
        elif argumentType == self._IMMED:
            return arg
        elif argumentType == self._HEX:  # B is digit
            return int(arg[:-1], 16)
        elif argumentType == self._INT:
            return int(arg)
        elif argumentType == self._LOCALVAR:
            return int(self.assembler.getLocalVar(arg))
        elif argumentType == self._BSS:
            return int(self.assembler.getFromMemoryAddress(self.assembler.getBSS()[arg][0]))
        elif argumentType == self._DATA:
            return int(self.assembler.getFromMemoryAddress(self.assembler.getDATA()[arg][0]))
        elif argumentType == self._LABEL:
            return self.assembler.getLabelFromLookupTable(arg)
        elif argumentType == self._CHAR:
            return ord(arg.strip("'").strip('"'))

    def setValue(self, arg, argType, to):
        if argType == self._REG8:
            if to >= 256:
                while to >= 256:
                    to -= 512
                self.assembler.setFlag('O')
            elif to < -256:
                while to < -256:
                    to += 512
                self.assembler.setFlag('O')

            self.assembler.setEightBitRegister(arg, to)
        elif argType == self._REG:  # Each regster is 2 bytes
            if to >= 2 ** 15:
                while to >= 2 ** 15:
                    to -= 2 ** 16
                self.assembler.setFlag('O')
            elif to < -2 ** 15:
                while to < -2 ** 15:
                    to += 2 ** 16
                self.assembler.setFlag('O')

            self.assembler.setRegister(arg, to)
        elif argType == self._BSS:  # each memory cell is 1 byte
            if to >= 256:
                while to >= 256:
                    to -= 512
                self.assembler.setFlag('O')
            elif to < -256:
                while to < -256:
                    to += 512
                self.assembler.setFlag('O')

            self.assembler.setMemoryAddress(self.assembler.getBSS()[arg][0], to)
        elif argType == self._DATA:  # Each memory cell is 1 byte
            if to >= 256:
                while to >= 256:
                    to -= 512
                self.assembler.setFlag('O')
            elif to < -256:
                while to < -256:
                    to += 512
                self.assembler.setFlag('O')

            self.assembler.setMemoryAddress(self.assembler.getDATA()[arg][0], to)

    def wrongArgsError(self, command, i, args, numArg):
        argList = []
        if self._REG in args:
            argList.append("16 bit register")
        if self._REG8 in args:
            argList.append("8 bit register")
        if self._IMMED in args:
            argList.append("number")
            argList.append("local variable")
            argList.append("single character")
        if self._MEM in args:
            argList.append("memory location")
        if self._LABEL in args:
            argList.append("jump label")

        if len(argList) > 1:
            argStr = ", ".join(argList[:-1])
            argStr += ", and " + argList[-1]

        if len(argList) == 0:
            self.gui.outPut("Error on line %s. %s expected no arguments! Received %s." % command[numArg])
        else:
            self.gui.outPut("Error on line %s. %s expected %s %s as a %s argument. Received %s." % (i, command[0], "one of" * (len(argList) > 1), argStr, "first" if numArg == 1 else "second", command[numArg]))

        self.gui.stopRunning(-1)

"""   10 more to go
"CMP":2,  # Compare operands
"CMPSB":-1,  # Compare bytes in memory
"CMPSW":-1,  # Compare words in memory
"DIV":2,  # Unsigned divide 
"IDIV":1,  # Signed divide
"IMUL":1,  # Signed multiply
"LDS":2,  # Load pointer using DS
"LEA":2,  # Load effective address
"LES":2,  # Load ES with pointer
"MUL":2,  # Unsigned Multiply
"""
