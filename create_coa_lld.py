"""Create COA LLD xlsx from structured data."""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

rows = []
def add(mod, seq, name, slug, path, obj, out, fa, details, refs="", hld="", status="Published"):
    rows.append({"module_name": mod, "lu_sequence": seq, "lu_name": name, "slugs": slug, "learning_path": path, "learning_objectives": obj, "learning_outcomes": out, "fa_type": fa, "assessment_details": details, "references": refs, "hld_mapping": hld, "completion_status": status})

M1 = "Introduction to Computer Organization and Architecture"
M2 = "Central Processing Unit Design and Instruction Execution"
M3 = "Pipelining and CPU Performance"
M4 = "Memory and Input/Output Organization"
M5 = "Modern Computing Systems and Specialized Architectures"

# Module 1
add(M1, "1.1", "Computer Organization and Architecture | Course Orientation", "lu2090001", "Mandatory",
    "- Understanding the role of Computer Organization and Architecture\n- Difference between Computer Architecture and Computer Organization\n- Relationship between hardware and software\n- Overview of CPU, memory, storage, and I/O components\n- How programs execute inside a computer system",
    "Explain how computer organization and architecture work together to connect software execution with hardware behavior inside a computer system.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-tutorials/", "Introduction & Curiosity Ignition")

add(M1, "1.1.1", "Computer Evolution: Historical Development and Generations of Computers", "lu2090002", "Bonus",
    "- Early mechanical computing devices\n- First generation computers and vacuum tubes\n- Second generation and transistor technology\n- Third generation and integrated circuits\n- Fourth and fifth generation computing systems\n- Evolution of speed, size, storage, and usability",
    "Describe how advances in hardware technologies influenced the evolution of modern computer systems across different generations.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.javatpoint.com/generations-of-computers")

add(M1, "1.2", "Von Neumann and Harvard System Models", "lu2090003", "Mandatory",
    "- Stored program concept\n- Components of Von Neumann architecture\n- Instruction and data flow in Von Neumann systems\n- Harvard architecture and separate memory organization\n- Comparison between Von Neumann and Harvard models\n- Real-world applications of both architectures",
    "Compare Von Neumann and Harvard architectures based on memory organization, instruction flow, and real-world applications.",
    "Assignment", "Type: Subjective\nDetails: Compare Von Neumann and Harvard architectures based on memory organization, execution flow, advantages, limitations, and real-world usage examples.",
    "https://www.geeksforgeeks.org/difference-between-von-neumann-and-harvard-architecture/")

add(M1, "1.3", "Computer Functional Units: CPU, Memory, I/O, and Bus Structures", "lu2090004", "Mandatory",
    "- Functional units of a computer system\n- CPU and its responsibilities\n- Memory organization and data storage\n- Input and output operations\n- Bus structures and internal communication\n- Data flow between functional units",
    "Describe how CPU, memory, I/O devices, and buses coordinate to execute programs and transfer data inside a computer system.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.tutorialspoint.com/computer_logical_organization/functional_units_of_computer_system.htm")

add(M1, "1.3.1", "Assignment | Computer Functional Units", "lu2090004_1", "Bonus",
    "Practice-based subjective assignment on computer functional units",
    "Strengthen understanding of computer functional units through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M1, "1.4", "Number Systems", "coa4_v3_lu5", "Mandatory",
    "- Decimal number system fundamentals\n- Binary number representation\n- Octal and hexadecimal systems\n- Conversion between number systems\n- Arithmetic operations in binary\n- Applications of number systems in computing",
    "Convert and interpret values across binary, octal, decimal, and hexadecimal number systems used in computing.",
    "Assignment", "Type: Subjective\nDetails: Solve conversion problems involving binary, octal, decimal, and hexadecimal number systems with step-by-step working.",
    "https://www.javatpoint.com/number-system-in-computer")

add(M1, "1.4.1", "Binary Codes", "coa4_v3_lu6", "Bonus",
    "- Character representation using ASCII\n- Decimal representation using BCD\n- Gray code generation and applications\n- Excess-3 code representation\n- Error detection using parity bits\n- Applications of binary coding schemes",
    "Apply binary coding schemes such as ASCII, BCD, Gray code, and parity bits to represent and validate data in computer systems.",
    "Assignment", "Type: File Upload\nDetails: Submit solved exercises involving ASCII encoding, BCD conversion, Gray code generation, Excess-3 conversion, and parity checking.",
    "https://www.geeksforgeeks.org/binary-codes-in-digital-electronics/")

add(M1, "1.5", "Signed Number Representation", "coa4_v3_lu7", "Mandatory",
    "- Representation of signed numbers\n- Sign-magnitude representation\n- 1's complement representation\n- 2's complement representation\n- Binary addition and subtraction\n- Overflow concepts in binary arithmetic",
    "Solve binary arithmetic problems involving signed number representations using complement systems.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/difference-between-1s-complement-representation-and-2s-complement-representation-technique/")

add(M1, "1.5.1", "Logic Gates and Boolean Algebra", "coa4_v3_lu8", "Bonus",
    "- Introduction to digital logic gates\n- AND, OR, NOT, NAND, NOR, XOR gates\n- Truth tables and logical operations\n- Boolean expressions and simplification\n- De Morgan's laws\n- Applications of Boolean algebra in circuits",
    "Apply Boolean operations and analyze the behavior of digital logic gates used in circuit design.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.tutorialspoint.com/computer_logical_organization/logic_gates.htm")

add(M1, "1.6", "Registers and Common Bus Organization", "coa4_v3_lu9", "Mandatory",
    "- Introduction to CPU registers\n- Types and functions of registers\n- Register transfer operations\n- Common bus organization concepts\n- Data movement between registers\n- Internal CPU communication mechanisms",
    "Explain how registers and common bus organization support internal data movement within the CPU.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/registers-in-computer-organization/")

add(M1, "1.6.1", "Assignment | Registers and Common Bus Organization", "coa4_v3_lu9_1", "Bonus",
    "Practice-based subjective assignment on registers and common bus organization",
    "Strengthen understanding of registers and common bus organization through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M1, "1.7", "Instruction Set Architecture and RISC vs CISC Design", "coa4_v3_lu10", "Mandatory",
    "- Introduction to ISA\n- Instructions and operands\n- Role of registers in instruction execution\n- Hardware-software interface concepts\n- Types of instructions in a processor\n- Real-world ISA examples\n- Open-source ISA concepts and introduction to RISC-V\n- Comparison of ARM, x86, and RISC-V architectures\n- Real-world adoption of RISC-V in embedded and AI systems",
    "Explain how instruction sets define communication between software instructions and processor hardware.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.arm.com/glossary/isa https://www.geeksforgeeks.org/computer-organization-risc-and-cisc/")

add(M1, "1.8", "Flynn's Classification of Parallel Computer Systems", "coa4_v3_lu11", "Mandatory",
    "- Introduction to parallel processing\n- SISD architecture\n- SIMD architecture\n- MISD architecture\n- MIMD architecture\n- Applications of parallel computing systems",
    "Classify computer systems using Flynn's taxonomy based on different parallel processing approaches.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-flynns-taxonomy/")

add(M1, "1.8.1", "Assignment | Flynn's Classification of Parallel Computer Systems", "coa4_v3_lu11_1", "Bonus",
    "Practice-based subjective assignment on Flynn's classification",
    "Strengthen understanding of Flynn's classification through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M1, "1.8.2", "Assignment | Processor Architectures and Parallel Computing", "coa4_v3_lu12", "Bonus",
    "- Applying ISA concepts to processor behavior\n- Comparing RISC and CISC execution models\n- Identifying Flynn's Classification in modern systems\n- Relating processor architectures to GPUs, multicore CPUs, and embedded devices\n- Connecting architecture choices with performance and efficiency",
    "Analyze processor architectures and parallel computing models by relating instruction set design and execution approaches to real-world computing systems.",
    "Assignment", "Type: Subjective\nDetails: Select a real-world computing device or processor and analyze its architecture.",
    "https://www.geeksforgeeks.org/computer-organization-risc-and-cisc/ https://www.geeksforgeeks.org/computer-organization-flynns-taxonomy/")

add(M1, "1.8.3", "Introduction to Embedded Systems and Microcontrollers", "coa4_v3_lu13", "Bonus",
    "- Introduction to embedded systems\n- Difference between general-purpose computers and embedded systems\n- Basics of microcontrollers and their components\n- Sensors, actuators, and control mechanisms\n- Real-world embedded system applications\n- Embedded systems in IoT and smart devices",
    "Explain how embedded systems and microcontrollers support dedicated computing operations in real-world applications.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/introduction-of-embedded-systems-set-1/")

# Module 2
add(M2, "2.1", "The Instruction Cycle", "coa4_v3_lu14", "Mandatory",
    "- Overview of instruction execution\n- Program Counter and Instruction Register\n- Fetch cycle operations\n- Decode cycle operations\n- Execute cycle operations\n- Write-back stage and result storage",
    "Explain how instructions move through fetch, decode, execute, and write-back stages during CPU execution.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/instruction-cycle-in-computer-organization/")

add(M2, "2.2", "Instruction Formats and Instruction Types", "coa4_v3_lu15", "Mandatory",
    "- Structure of instruction formats\n- Opcode and operand fields\n- Fixed-length and variable-length instructions\n- Arithmetic instructions\n- Data transfer instructions\n- Control and branching instructions",
    "Interpret instruction formats and classify processor instructions based on their operation types.",
    "Assignment", "Type: Subjective\nDetails: Analyze instruction formats and classify instructions based on operation type with suitable examples.",
    "https://www.geeksforgeeks.org/instruction-format-in-computer-architecture/")

add(M2, "2.3", "Addressing Modes", "coa4_v3_lu16", "Mandatory",
    "- Need for addressing modes\n- Immediate addressing mode\n- Direct and indirect addressing\n- Register addressing mode\n- Indexed addressing mode\n- Effective address calculation",
    "Differentiate addressing modes and explain how processors access operands during instruction execution.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/addressing-modes/")

add(M2, "2.3.1", "Assignment | Addressing Modes", "coa4_v3_lu16_1", "Bonus",
    "Practice-based subjective assignment on addressing modes",
    "Strengthen understanding of addressing modes through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M2, "2.3.2", "Branch Instructions and Program Control Flow", "coa4_v3_lu17", "Bonus",
    "- Introduction to control flow\n- Conditional branch instructions\n- Unconditional jump instructions\n- Program Counter modification\n- Looping and decision-making in programs\n- Applications of branching mechanisms",
    "Explain how branch instructions modify program execution flow and processor control behavior.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/control-instructions-in-computer-organization/")

add(M2, "2.3.3", "Assembly Language Programming and Instruction Sequencing", "coa4_v3_lu18", "Bonus",
    "- Basics of assembly language programming\n- Assembly instruction structure\n- Register usage in assembly programs\n- Labels and symbolic references\n- Instruction sequencing and execution order\n- Control flow implementation in assembly",
    "Trace instruction sequencing and execution behavior in simple assembly language programs.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.tutorialspoint.com/assembly_programming/index.htm")

add(M2, "2.4", "Hands-on: Tracing Instruction Execution with CPU Simulator", "coa4_v3_lu19", "Mandatory",
    "- Introduction to CPU simulator environment\n- Loading and executing instructions\n- Step-by-step instruction tracing\n- Register value observation\n- Memory update tracking\n- Analyzing execution behavior",
    "Trace instruction execution using a CPU simulator and analyze changes in register and memory states.",
    "Assignment", "Type: File upload\nDetails: Execute assembly instructions using a CPU simulator and submit screenshots with execution observations.",
    "https://cpulator.01xz.net/", "First Breakthrough")

add(M2, "2.5", "Data Path Design and Execution Flow", "coa4_v3_lu20", "Mandatory",
    "- Introduction to datapath architecture\n- Register file operations\n- Role of ALU in execution\n- Multiplexers and control signals\n- Instruction execution flow\n- Coordination between datapath components",
    "Describe how datapath components coordinate instruction execution inside a processor.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/data-path-design-in-computer-architecture/")

add(M2, "2.5.1", "Assignment | Data Path Design and Execution Flow", "coa4_v3_lu20_1", "Bonus",
    "Practice-based subjective assignment on data path design",
    "Strengthen understanding of data path design through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M2, "2.5.2", "Microoperations and Register Transfer Language (RTL)", "coa4_v3_lu21", "Bonus",
    "- Introduction to microoperations\n- Register transfer concepts\n- RTL notation and syntax\n- Arithmetic and logic microoperations\n- Data movement between registers\n- RTL representation of processor operations",
    "Interpret RTL statements and explain how microoperations control internal processor data movement.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/register-transfer-language-rtl/")

add(M2, "2.6", "Control Unit Design: Hardwired Control", "coa4_v3_lu22", "Mandatory",
    "- Role of the control unit\n- Hardwired control organization\n- Generation of control signals\n- Logic circuit implementation\n- Advantages and limitations of hardwired control\n- Applications in processor design",
    "Explain how hardwired control units generate and manage processor control signals.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/difference-between-hardwired-and-microprogrammed-control-unit/")

add(M2, "2.7", "Control Unit Design: Microprogrammed Control", "coa4_v3_lu23", "Mandatory",
    "- Introduction to microprogrammed control\n- Control memory organization\n- Microinstructions and control words\n- Sequencing of microoperations\n- Execution using control memory\n- Comparison with hardwired control",
    "Explain how microprogrammed control units execute instructions using control memory and microoperations.",
    "Assignment", "Type: Subjective\nDetails: Compare microprogrammed control with hardwired control using execution examples and architecture diagrams.",
    "https://www.geeksforgeeks.org/difference-between-hardwired-and-microprogrammed-control-unit/")

add(M2, "2.7.1", "Assignment | Control Unit Design", "coa4_v3_lu23_1", "Bonus",
    "Practice-based subjective assignment on control unit design",
    "Strengthen understanding of control unit design through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M2, "2.7.2", "Comparing Control Unit Designs: Trade-offs and Real-World Practice", "coa4_v3_lu24", "Bonus",
    "- Hardwired vs microprogrammed control overview\n- Performance trade-offs\n- Hardware complexity and flexibility\n- RISC and CISC control approaches\n- Real-world processor examples\n- Design decision analysis",
    "Compare hardwired and microprogrammed control units based on flexibility, performance, and hardware complexity.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/difference-between-hardwired-and-microprogrammed-control-unit/")

add(M2, "2.7.3", "Interrupts and Interrupt Handling Mechanism", "coa4_v3_lu25", "Bonus",
    "- Introduction to interrupts\n- Types of interrupts\n- Interrupt cycle and processing\n- Interrupt Service Routine (ISR)\n- Context switching mechanisms\n- Applications of interrupts in systems",
    "Explain how processors detect, handle, and respond to interrupts during execution.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/interrupts-in-computer-organization-architecture/")

add(M2, "2.8", "Case Study: x86, MIPS, and RISC-V Instruction Set Architectures", "coa4_v3_lu26", "Mandatory",
    "- Overview of x86 architecture\n- Overview of MIPS architecture\n- Introduction to RISC-V architecture\n- Register organization in processors\n- Instruction encoding formats\n- Execution behavior comparison\n- Comparison between x86, MIPS, and RISC-V\n- Open-source ISA design principles\n- Real-world processor design decisions\n- RISC-V applications in embedded and AI systems",
    "Analyze instruction execution behavior and architectural design decisions in x86, MIPS, and RISC-V processors.",
    "Assignment", "Type: Subjective\nDetails: Analyze instruction execution and architectural design decisions in x86, RISC-V or MIPS processors.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-mips-architecture/")

# Module 3
add(M3, "3.1", "Pipelining: Stages, Throughput, and Speedup", "coa4_v3_lu27", "Mandatory",
    "- Introduction to pipelining\n- Sequential vs pipelined execution\n- Pipeline stages and instruction overlap\n- Pipeline throughput improvement\n- Pipeline speedup concepts\n- Real-world pipeline examples",
    "Explain how pipelining improves instruction execution efficiency and increases processor throughput.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-1-execution-stages-and-throughput/")

add(M3, "3.1.1", "Assignment | Pipelining: Concept, Stages, Throughput, and Speedup", "coa4_v3_lu27_1", "Bonus",
    "Practice-based subjective assignment on pipelining concepts",
    "Strengthen understanding of pipelining concepts through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M3, "3.2", "Pipeline Performance Parameters", "coa4_v3_lu28", "Mandatory",
    "- Pipeline depth and stage balancing\n- Clock cycle time in pipelines\n- CPI in pipelined processors\n- Pipeline latency and throughput\n- Performance trade-offs in pipeline design\n- Pipeline efficiency calculations",
    "Calculate and interpret pipeline performance metrics such as CPI, throughput, and execution time.",
    "Assignment", "Type: Subjective\nDetails: Solve problems involving pipeline depth, CPI, clock cycles, throughput, and execution time analysis.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/")

add(M3, "3.2.1", "Asynchronous Pipeline Design", "coa4_v3_lu29", "Bonus",
    "- Synchronized vs non-synchronized pipelines\n- Asynchronous pipeline execution\n- Timing challenges in pipelines\n- Pipeline coordination mechanisms\n- Advantages and limitations of asynchronous design\n- Applications in modern processors",
    "Explain asynchronous and non-synchronized pipeline execution concepts and their design challenges.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-1-execution-stages-and-throughput/")

add(M3, "3.3", "Structural Hazards", "coa4_v3_lu30", "Mandatory",
    "- Introduction to pipeline hazards\n- Structural hazard concepts\n- Resource conflicts in pipelines\n- Hazard detection mechanisms\n- Stalling and hardware duplication\n- Structural hazard resolution techniques",
    "Identify structural hazards in pipelined processors and explain techniques used to resolve hardware resource conflicts.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/")

add(M3, "3.3.1", "Assignment | Structural Hazards", "coa4_v3_lu30_1", "Bonus",
    "Practice-based subjective assignment on structural hazards",
    "Strengthen understanding of structural hazards through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M3, "3.4", "Data Hazards", "coa4_v3_lu31", "Mandatory",
    "- Introduction to data dependencies\n- RAW hazards\n- WAR hazards\n- WAW hazards\n- Pipeline stalling concepts\n- Data forwarding and bypassing techniques",
    "Differentiate RAW, WAR, and WAW hazards and apply suitable hazard mitigation techniques in pipelined execution.",
    "Assignment", "Type: Subjective\nDetails: Analyze pipelined instruction sequences and identify RAW, WAR, and WAW hazards with suitable mitigation techniques.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/", "Second Breakthrough")

add(M3, "3.4.1", "Advanced Hazard Resolution", "coa4_v3_lu32", "Bonus",
    "- Advanced stalling techniques\n- Data bypassing mechanisms\n- Instruction reordering concepts\n- Dynamic scheduling basics\n- Pipeline optimization strategies\n- Hazard minimization techniques",
    "Explain advanced hazard resolution techniques such as bypassing, instruction reordering, and dynamic scheduling.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/")

add(M3, "3.5", "Control Hazards", "coa4_v3_lu33", "Mandatory",
    "- Branch instructions in pipelines\n- Control hazard concepts\n- Branch penalties\n- Branch prediction basics\n- Delayed branching concepts\n- Control hazard mitigation techniques",
    "Explain how branch instructions create control hazards and affect pipeline execution performance.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/")

add(M3, "3.5.1", "Assignment | Control Hazards", "coa4_v3_lu33_1", "Bonus",
    "Practice-based subjective assignment on control hazards",
    "Strengthen understanding of control hazards through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M3, "3.5.2", "Branch Target Buffers and Speculative Execution", "coa4_v3_lu34", "Bonus",
    "- Branch target buffers\n- Dynamic branch prediction\n- Speculative execution concepts\n- Prediction accuracy and penalties\n- Pipeline rollback mechanisms\n- Applications in modern CPUs",
    "Explain how speculative execution and branch target buffers improve modern processor performance.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-branch-prediction/")

add(M3, "3.6", "Pipeline Performance Analysis with Hazards", "coa4_v3_lu35", "Mandatory",
    "- Hazard impact on CPI\n- Throughput reduction analysis\n- Stall cycle calculations\n- Pipeline efficiency analysis\n- Hazard performance trade-offs\n- Pipeline optimization evaluation",
    "Analyze how hazards reduce pipeline efficiency and impact processor performance metrics.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-3-stalls-and-forwarding/")

add(M3, "3.6.1", "Superscalar Processors and Out-of-Order Execution", "coa4_v3_lu36", "Bonus",
    "- Superscalar architecture basics\n- Multiple instruction issue\n- Out-of-order execution concepts\n- Dependency checking mechanisms\n- Instruction scheduling techniques\n- Modern processor execution models",
    "Explain how superscalar and out-of-order execution techniques improve instruction-level parallelism.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/superscalar-architecture/")

add(M3, "3.7", "CPU Performance Equation", "coa4_v3_lu37", "Mandatory",
    "- CPU performance equation fundamentals\n- Instruction count and execution time\n- CPI contribution to performance\n- Clock rate and cycle time\n- Performance comparison problems\n- Optimization trade-offs in CPU design",
    "Apply CPU performance equations to evaluate and compare processor efficiency.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-organization-and-architecture-performance-metrics/")

add(M3, "3.8", "Amdahl's Law and Optimization Limits", "coa4_v3_lu38", "Mandatory",
    "- Introduction to Amdahl's Law\n- Parallel and serial execution components\n- Speedup calculations\n- Optimization limitations\n- Real-world performance trade-offs\n- Evaluating architectural improvements",
    "Apply Amdahl's Law to evaluate optimization limits and performance improvement trade-offs.",
    "Assignment", "Type: Subjective\nDetails: Solve performance optimization problems using Amdahl's Law and analyze architectural trade-offs.",
    "https://www.geeksforgeeks.org/amdahls-law-and-its-proof/")

add(M3, "3.8.1", "Case Study: Pipelining Optimization in Modern Processors", "coa4_v3_lu39", "Bonus",
    "- Pipeline optimization in modern CPUs\n- Real-world hazard mitigation techniques\n- Speculative execution in processors\n- Performance optimization strategies\n- Processor design trade-offs\n- Case study analysis of modern architectures",
    "Analyze real-world pipelining optimization techniques used in modern processor architectures.",
    "Assignment", "Type: Subjective\nDetails: Analyze pipelining optimization techniques used in modern processors and evaluate their performance impact.",
    "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html")

# Module 4
add(M4, "4.1", "Introduction to Memory Organization", "coa4_v3_lu40", "Mandatory",
    "- Memory hierarchy overview\n- Primary and secondary memory\n- Registers, cache, RAM, and storage devices\n- Word size and addressing concepts\n- Memory access speed comparison\n- Performance implications of memory hierarchy",
    "Explain how memory hierarchy and storage characteristics influence computer system performance.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/memory-hierarchy-design-and-its-characteristics/")

add(M4, "4.2", "Cache Memory: Concept, Structure, and Hit-Miss Ratio", "coa4_v3_lu41", "Mandatory",
    "- Introduction to cache memory\n- Cache organization and structure\n- Cache blocks and cache lines\n- Cache hit and cache miss concepts\n- Hit ratio and miss ratio calculations\n- Cache performance improvement",
    "Explain cache organization and evaluate cache performance using hit and miss ratios.",
    "Assignment", "Type: Subjective\nDetails: Solve cache hit-miss ratio problems and analyze cache performance in different execution scenarios.",
    "https://www.geeksforgeeks.org/cache-memory-in-computer-organization/")

add(M4, "4.2.1", "Average Access Time and Memory Performance Metrics", "coa4_v3_lu42", "Bonus",
    "- Average access time concepts\n- Cache access latency\n- Miss penalty calculation\n- CPI impact of cache misses\n- Memory performance equations\n- System performance trade-offs",
    "Calculate average memory access time and analyze the impact of cache performance on CPU efficiency.",
    "Assignment", "Type: Subjective\nDetails: Calculate average memory access time and analyze cache miss penalties using performance equations.",
    "https://www.geeksforgeeks.org/cache-memory-in-computer-organization/")

add(M4, "4.3", "Cache Mapping Techniques: Direct Mapping", "coa4_v3_lu43", "Mandatory",
    "- Introduction to cache mapping\n- Direct mapping organization\n- Tag, index, and offset fields\n- Address breakdown concepts\n- Cache block placement\n- Direct mapping advantages and limitations",
    "Explain direct cache mapping and perform memory block placement calculations.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/difference-between-direct-mapping-associative-mapping-set-associative-mapping/")

add(M4, "4.3.1", "Assignment | Direct Mapping", "coa4_v3_lu43_1", "Bonus",
    "Practice-based subjective assignment on direct mapping",
    "Strengthen understanding of direct mapping through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M4, "4.4", "Cache Mapping Techniques: Associative and Set-Associative Mapping", "coa4_v3_lu44", "Mandatory",
    "- Associative mapping concepts\n- Fully associative cache organization\n- Set-associative cache structure\n- Cache searching mechanisms\n- Mapping efficiency comparison\n- Hardware complexity trade-offs",
    "Differentiate associative and set-associative cache mapping techniques based on efficiency and hardware complexity.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/difference-between-direct-mapping-associative-mapping-set-associative-mapping/")

add(M4, "4.5", "Cache Replacement Policies", "coa4_v3_lu45", "Mandatory",
    "- Cache replacement concepts\n- Least Recently Used (LRU)\n- First In First Out (FIFO)\n- Random replacement policy\n- Replacement decision mechanisms\n- Performance comparison of replacement strategies",
    "Explain cache replacement strategies such as LRU, FIFO, and random replacement policies.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/cache-replacement-policies-system-design/")

add(M4, "4.5.1", "Assignment | Cache Replacement Policies", "coa4_v3_lu45_1", "Bonus",
    "Practice-based subjective assignment on cache replacement policies",
    "Strengthen understanding of cache replacement policies through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M4, "4.6", "Cache Write Policies", "coa4_v3_lu46", "Mandatory",
    "- Cache write operations\n- Write-through policy\n- Write-back policy\n- Dirty bit concepts\n- Memory consistency considerations\n- Write policy performance trade-offs",
    "Differentiate write-through and write-back cache policies and analyze their performance trade-offs.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/cache-write-policies-system-design/")

add(M4, "4.6.1", "Assignment | Cache Write Policies", "coa4_v3_lu46_1", "Bonus",
    "Practice-based subjective assignment on cache write policies",
    "Strengthen understanding of cache write policies through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M4, "4.6.2", "Multi-Level Cache Architecture", "coa4_v3_lu47", "Bonus",
    "- Multi-level cache hierarchy\n- L1 cache characteristics\n- L2 cache organization\n- L3 shared cache concepts\n- Cache coordination mechanisms\n- Performance optimization using cache levels",
    "Explain the organization and performance roles of L1, L2, and L3 cache systems in modern processors.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/multilevel-cache-organisation/")

add(M4, "4.7", "I/O Techniques: Programmed I/O, Interrupt-Driven I/O, and DMA", "coa4_v3_lu48", "Mandatory",
    "- Introduction to I/O systems\n- Programmed I/O operation\n- Interrupt-driven I/O concepts\n- Direct Memory Access (DMA)\n- CPU involvement in I/O operations\n- Performance comparison of I/O techniques",
    "Compare programmed I/O, interrupt-driven I/O, and DMA techniques based on execution flow and CPU utilization.",
    "Assignment", "Type: Subjective\nDetails: Compare programmed I/O, interrupt-driven I/O, and DMA based on execution flow, CPU utilization, and performance.",
    "https://www.geeksforgeeks.org/modes-of-transfer-programmed-io-and-interrupt-initiated-io/")

add(M4, "4.8", "DMA Controller and System Bus Interaction", "coa4_v3_lu49", "Mandatory",
    "- DMA controller architecture\n- Bus arbitration concepts\n- Data transfer coordination\n- Memory-device communication\n- DMA transfer modes\n- System bus interaction mechanisms",
    "Explain how DMA controllers coordinate data transfer and interact with system buses.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/direct-memory-access-dma-controller-in-computer-architecture/")

add(M4, "4.8.1", "Virtual Memory: Concepts, Paging, and Page Replacement", "coa4_v3_lu50", "Bonus",
    "- Virtual memory concepts\n- Paging and page tables\n- Logical and physical addresses\n- Page faults and swapping\n- Page replacement algorithms\n- Memory management efficiency",
    "Explain paging, virtual memory organization, and page replacement mechanisms used in memory management.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/virtual-memory-in-operating-system/")

add(M4, "4.9", "Hands-on: Cache Simulation and Memory Performance Analysis", "coa4_v3_lu51", "Mandatory",
    "- Cache simulation environment\n- Configuring cache parameters\n- Analyzing cache hit and miss behavior\n- Evaluating replacement policies\n- Measuring memory performance metrics\n- Interpreting cache simulation results",
    "Analyze cache behavior and evaluate memory system performance using simulation-based experiments.",
    "Assignment", "Type: File Upload\nDetails: Perform cache simulation experiments, analyze cache performance metrics, and submit observations with screenshots and performance analysis.",
    "https://www.cs.virginia.edu/~cr4bd/3130/S2024/labhw/cache-programs.html", "Deep Immersion")

add(M4, "4.9.1", "Case Study: ARM Architecture - ISA, Instruction Encoding, Memory, and I/O", "coa4_v3_lu52", "Bonus",
    "- ARM ISA overview\n- Instruction encoding in ARM processors\n- Memory organization in ARM architecture\n- ARM I/O mechanisms\n- Cache and performance optimization in ARM\n- Real-world ARM processor applications",
    "Analyze ARM architecture features related to instruction encoding, memory organization, cache behavior, and I/O systems.",
    "Assignment", "Type: Subjective\nDetails: Analyze ARM processor architecture focusing on ISA, instruction encoding, memory organization, cache behavior, and I/O mechanisms.",
    "https://developer.arm.com/documentation")

# Module 5
add(M5, "5.1", "Specialized Computing Systems and Modern Workloads", "coa4_v3_lu53", "Mandatory",
    "- Evolution from general-purpose to specialized computing systems\n- Modern computing workloads and processing demands\n- Workload-driven hardware design concepts\n- Gaming, AI, cloud, and scientific workloads\n- Specialized processors and accelerators\n- Real-world examples of modern computing systems",
    "Explain how specialized computing systems are designed to address modern workloads such as gaming, AI, cloud computing, and scientific applications.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/computer-architecture-tutorial/")

add(M5, "5.2", "GPU Computing Architecture for Graphics and AI", "coa4_v3_lu54", "Mandatory",
    "- Introduction to GPU computing\n- GPU cores and parallel execution\n- Graphics rendering fundamentals\n- GPU processing pipelines\n- AI and scientific computing applications\n- CPU vs GPU workload characteristics",
    "Explain how GPU architectures improve parallel processing efficiency in graphics rendering and AI workloads.",
    "Assignment", "Type: Subjective\nDetails: Analyze GPU architecture and explain how parallel execution improves graphics rendering and AI workload performance.",
    "https://www.geeksforgeeks.org/what-is-gpu/")

add(M5, "5.2.1", "Graphics Rendering Pipelines and Real-Time Processing", "coa4_v3_lu55", "Bonus",
    "- Stages in graphics rendering pipelines\n- Vertex and fragment processing concepts\n- Real-time rendering fundamentals\n- Frame generation and display concepts\n- Latency and rendering performance\n- Applications in gaming and visualization",
    "Understand how graphics rendering pipelines process and display real-time visual content efficiently.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://developer.nvidia.com/gpu-computing")

add(M5, "5.3", "AI Accelerators and Tensor Processing Units", "coa4_v3_lu56", "Mandatory",
    "- Introduction to AI accelerators\n- TPU architecture basics\n- Matrix and tensor operations\n- AI inference and training workloads\n- Hardware acceleration for machine learning\n- Applications of AI accelerator systems",
    "Explain how TPUs and AI accelerators improve matrix processing and machine learning computation efficiency.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://cloud.google.com/tpu/docs/system-architecture")

add(M5, "5.3.1", "Assignment | AI Accelerators and Tensor Processing Units", "coa4_v3_lu56_1", "Bonus",
    "Practice-based subjective assignment on AI accelerators",
    "Strengthen understanding of AI accelerators through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M5, "5.4", "Memory Bandwidth Challenges in Modern Computing Systems", "coa4_v3_lu57", "Mandatory",
    "- Memory bandwidth concepts\n- Data movement bottlenecks\n- GPU memory requirements\n- AI workload memory demands\n- Throughput limitations in modern systems\n- Performance implications of bandwidth constraints",
    "Learn how memory bandwidth influences the performance of GPUs, AI accelerators, and high-performance systems.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/memory-hierarchy-design-and-its-characteristics/")

add(M5, "5.4.1", "High-Bandwidth Memory and Unified Memory Architectures", "coa4_v3_lu58", "Bonus",
    "- High-bandwidth memory concepts\n- Unified memory architecture\n- Memory sharing between processors\n- Memory access optimization\n- Modern GPU memory systems\n- Applications in AI and gaming systems",
    "Explain how high-bandwidth memory and unified memory architectures improve modern system performance.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://developer.nvidia.com/blog/unified-memory-cuda-beginners/")

add(M5, "5.4.2", "Assignment | Memory Bandwidth Challenges", "coa4_v3_lu58_1", "Bonus",
    "Practice-based subjective assignment on memory bandwidth challenges",
    "Strengthen understanding of memory bandwidth challenges through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M5, "5.5", "Thermal Management and Cooling in High-Performance Systems", "coa4_v3_lu59", "Mandatory",
    "- Heat generation in computing systems\n- Thermal throttling concepts\n- Air cooling and liquid cooling methods\n- Heat sinks and thermal design\n- Cooling challenges in gaming and AI systems\n- Reliability and performance considerations",
    "Explain how thermal management and cooling systems maintain performance and reliability in modern computing devices.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.intel.com/content/www/us/en/gaming/resources/pc-cooling-the-ultimate-guide.html")

add(M5, "5.5.1", "Assignment | Thermal Management and Cooling", "coa4_v3_lu59_1", "Bonus",
    "Practice-based subjective assignment on thermal management and cooling",
    "Strengthen understanding of thermal management and cooling through practice-based subjective assignment",
    "Assignment", "Type: Subjective\nDetails: Case study/application based subjective questions for practice")

add(M5, "5.6", "Energy-Efficient Computing and Power Optimization", "coa4_v3_lu60", "Mandatory",
    "- Power consumption in computing systems\n- Dynamic voltage and frequency scaling\n- Power-performance trade-offs\n- Energy-efficient processor design\n- Battery and mobile device considerations\n- Power optimization in modern architectures",
    "Explain how power optimization techniques improve efficiency in mobile, embedded, and high-performance systems.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.geeksforgeeks.org/power-consumption-in-computer-architecture/")

add(M5, "5.6.1", "Assignment | Energy-Efficient Computing and Power Optimization", "coa4_v3_lu61", "Bonus",
    "- Applying power optimization concepts in real-world systems\n- Evaluating energy-efficient processor techniques\n- Comparing power-performance trade-offs\n- Analyzing efficiency challenges in mobile, embedded, AI, and high-performance systems",
    "Analyze how power optimization techniques improve efficiency, performance, and reliability in modern computing systems.",
    "Assignment", "Type: Subjective\nDetails: Select a modern computing system and analyze power optimization techniques.",
    "https://www.geeksforgeeks.org/power-consumption-in-computer-architecture/")

add(M5, "5.7", "Architecture of Edge Computing and Embedded AI Hardware", "coa4_v3_lu62", "Mandatory",
    "- Introduction to edge computing hardware\n- Embedded AI processor concepts\n- Local real-time processing systems\n- Hardware acceleration in edge devices\n- IoT and smart device architectures\n- Performance constraints in edge systems",
    "Explain how edge computing systems and embedded AI hardware support efficient real-time local processing.",
    "Assignment", "Type: Subjective\nDetails: Analyze how edge computing devices use specialized hardware architectures for real-time local processing in IoT or AI applications.",
    "https://www.geeksforgeeks.org/what-is-edge-computing/")

add(M5, "5.8", "Scalable Computing Architectures in Data Centers", "coa4_v3_lu63", "Mandatory",
    "- Introduction to data center architectures\n- Server hardware organization\n- Scalable computing systems\n- Distributed hardware resources\n- High-performance storage and networking\n- Reliability and scalability considerations",
    "Explain how scalable computing architectures support high-performance and large-scale data center operations.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://azure.microsoft.com/en-in/resources/cloud-computing-dictionary/what-is-a-data-center")

add(M5, "5.8.1", "Case Study: Apple Silicon and Modern System-on-Chip (SoC) Design", "coa4_v3_lu64", "Bonus",
    "- Introduction to System-on-Chip design\n- Apple Silicon architecture overview\n- CPU, GPU, and memory integration\n- Unified memory concepts\n- Performance and efficiency optimization\n- Real-world applications of SoC systems",
    "Analyze how System-on-Chip architectures improve integration, efficiency, and performance in modern computing devices.",
    "Assignment", "Type: Subjective\nDetails: Analyze Apple Silicon architecture and explain how System-on-Chip integration improves performance and efficiency.",
    "https://developer.apple.com/documentation/apple-silicon")

add(M5, "5.9", "Emerging Hardware Architectures for Next-Generation Computing", "coa4_v3_lu65", "Mandatory",
    "- Future hardware architecture trends\n- Quantum-inspired computing concepts\n- Neuromorphic hardware basics\n- AI-driven processor evolution\n- Specialized future computing systems\n- Challenges in next-generation architecture design",
    "Explain how emerging hardware architectures may influence future computing performance, efficiency, and system design approaches.",
    "Quiz", "Type: Progress Quiz\nDetails: A bank of 15 MCQs will be available. 5 questions will be randomly presented to the student.",
    "https://www.ibm.com/topics/quantum-computing")

add(M5, "5.9.1", "Assignment | Specialized Hardware Architecture Analysis", "coa4_v3_lu66", "Bonus",
    "- Applying modern architecture concepts\n- Analyzing specialized computing systems\n- Evaluating workload optimization strategies\n- Relating memory and performance behavior\n- Examining power and thermal considerations",
    "Analyze modern computing systems by relating architecture, performance, memory, and efficiency considerations to real-world applications.",
    "Assignment", "Type: Subjective\nDetails: Select a modern computing system and analyze its architecture, memory organization, performance optimization techniques, and efficiency considerations.",
    "https://www.nvidia.com/en-in/data-center/", "Mastery")

df = pd.DataFrame(rows)
df.to_excel(os.path.join(DATA_DIR, "COA_lld.xlsx"), index=False)
print(f"✅ Created COA_lld.xlsx — {len(df)} LUs")
