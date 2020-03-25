"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # ram = 256 bytes of memory
        self.ram = [0] * 256

        # registers = 8 general purpose
        self.reg = [0] * 8
        # program counter for any internal registers
        self.pc = 0
        # stack pointer
        self.sp = 7 


    def load(self):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0 
            cmd_file = sys.argv[1]

            # open file: save appropriate data to RAM
            with open(cmd_file) as f:

                # read the content line by line
                for line in f:

                    # remove '#' comments
                    cmd_split = line.split('#')

                    # remove spaces
                    cmd = cmd_split[0].strip()
                    
                    # ignore black lines
                    if cmd == '':
                        continue

                    # convert binary string to integer
                    value = int(cmd, 2)

                    # save data to RAM
                    self.ram[address] = value

                    # increment address'
                    address += 1

        except FileNotFoundError:
            print(f'Error: {cmd_file} file not found')
            sys.exit()




    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        # multiple two register values
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # The MAR contains the ADDRESS that is being read or written to
    # The MDR contains the data (VALUE) that was read or the data to write
    # You don’t need to add the MAR or MDR to your CPU class, 
    # but they would make handy paramter names for ram_read() and ram_write(), 
    # if you wanted.

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        # Pull these out?
        LDI  = 0b10000010
        PRN  = 0b01000111
        HLT  = 0b00000001
        MUL  = 0b10100010
        POP  = 0b01000110
        PUSH = 0b01000101

        running = True

        while running:
            
            # read memory address that is stored in register PC and store it in the Instruction Register
            IR = self.ram[self.pc]
            SP = self.sp

            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            # operand_a -> position of r0 (register and index 0) is 0b00000000 ==  to operand_b

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # halt / exit
            if IR == HLT:
                print('HALT!')
                running = False
                # self.pc += 1

            elif IR == PRN:
                reg = self.ram[self.pc + 1]
                print('register: ', self.reg[reg])   
                self.pc += 2

            # sets a specified register to a specified value
            elif IR == LDI:
                print('op a: ', operand_a, self.ram[operand_a]) # 0 
                print('op b: ', operand_b, self.ram[operand_b])
                # self.reg[operand_a] = operand_b
                reg = self.ram[self.pc + 1]
                print('reg: ', reg)
                val = self.ram[self.pc + 2]
                self.reg[reg] = val
                print('val: ', val)
                self.pc += 3

            # multiply the values using ALU
            elif IR == MUL:
                self.alu('MUL', operand_a,operand_b)
                self.pc += 3

            elif IR == POP:
                # register = first argument
                reg = operand_a

                # grab values we are putting on the register
                val = self.ram[self.reg[SP]]
                self.reg[reg] = val

                # increment SP
                self.reg[SP] += 1

                # increment PC by 2
                self.pc += 2 

            elif IR == PUSH:
                # register = first argument
                reg = operand_a

                # grab values we are putting on the register
                val = self.reg[reg]

                # decrement SP
                self.reg[SP] -= 1

                # copy/write value in given register to address pointed by SP 
                self.ram_write(self.reg[SP], val)

                # increment PC by 2
                self.pc += 2

            else:
                print(f"Unknown instruction: {IR}")
                sys.exit(1)

