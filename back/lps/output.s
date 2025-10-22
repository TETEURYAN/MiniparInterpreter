CÓDIGO INTERMEDIÁRIO (3 ENDEREÇOS):
--------------------------------------------------
  1: LOAD_VAR
      Destino: t0
      Arg1: Exemplo

  2: LOAD_VAR
      Destino: t1
      Arg1: de

  3: LOAD_VAR
      Destino: t2
      Arg1: c

  4: LOAD_VAR
      Destino: t3
      Arg1: digo

  5: LOAD_VAR
      Destino: t4
      Arg1: Minipar

  6: LOAD_VAR
      Destino: t5
      Arg1: Este

  7: LOAD_VAR
      Destino: t6
      Arg1: arquivo

  8: LOAD_VAR
      Destino: t7
      Arg1: demonstra

  9: LOAD_VAR
      Destino: t8
      Arg1: as

 10: LOAD_VAR
      Destino: t9
      Arg1: principais

 11: LOAD_VAR
      Destino: t10
      Arg1: caracter

 12: LOAD_VAR
      Destino: t11
      Arg1: sticas

 13: LOAD_VAR
      Destino: t12
      Arg1: da

 14: LOAD_VAR
      Destino: t13
      Arg1: linguagem

 15: LOAD_VAR
      Destino: t14
      Arg1: a

 16: LOAD_CONST
      Destino: t15
      Arg1: 5

 17: LOAD_VAR
      Destino: t16
      Arg1: b

 18: LOAD_CONST
      Destino: t17
      Arg1: 10

 19: LOAD_VAR
      Destino: t18
      Arg1: c

 20: LOAD_VAR
      Destino: t19
      Arg1: a

 21: LOAD_VAR
      Destino: t20
      Arg1: b

 22: LOAD_VAR
      Destino: t21
      Arg1: a

 23: LOAD_VAR
      Destino: t22
      Arg1: b

 24: LOAD_VAR
      Destino: t23
      Arg1: c

 25: LOAD_VAR
      Destino: t24
      Arg1: Estrutura

 26: LOAD_VAR
      Destino: t25
      Arg1: de

 27: LOAD_VAR
      Destino: t26
      Arg1: controle

 28: LOAD_VAR
      Destino: t27
      Arg1: a

 29: LOAD_VAR
      Destino: t28
      Arg1: b

 30: LOAD_CONST
      Destino: t29
      Arg1: "a é maior que b"

 31: LOAD_CONST
      Destino: t30
      Arg1: "b é maior ou igual a a"

 32: LOAD_VAR
      Destino: t31
      Arg1: Loop

 33: LOAD_VAR
      Destino: t32
      Arg1: i

 34: LOAD_CONST
      Destino: t33
      Arg1: 0

 35: LOAD_VAR
      Destino: t34
      Arg1: i

 36: LOAD_CONST
      Destino: t35
      Arg1: 5

 37: LOAD_VAR
      Destino: t36
      Arg1: i

 38: LOAD_VAR
      Destino: t37
      Arg1: i

 39: LOAD_VAR
      Destino: t38
      Arg1: i

 40: LOAD_CONST
      Destino: t39
      Arg1: 1

 41: LOAD_VAR
      Destino: t40
      Arg1: Loop

 42: LOAD_VAR
      Destino: t41
      Arg1: j

 43: LOAD_CONST
      Destino: t42
      Arg1: 0

 44: LOAD_VAR
      Destino: t43
      Arg1: j

 45: LOAD_CONST
      Destino: t44
      Arg1: 3

 46: LOAD_VAR
      Destino: t45
      Arg1: j

 47: LOAD_VAR
      Destino: t46
      Arg1: j

 48: LOAD_CONST
      Destino: t47
      Arg1: 1

 49: LOAD_VAR
      Destino: t48
      Arg1: j

 50: LOAD_VAR
      Destino: t49
      Arg1: Opera

 51: LOAD_VAR
      Destino: t50
      Arg1: es

 52: LOAD_VAR
      Destino: t51
      Arg1: aritm

 53: LOAD_VAR
      Destino: t52
      Arg1: ticas

 54: LOAD_VAR
      Destino: t53
      Arg1: x

 55: LOAD_CONST
      Destino: t54
      Arg1: 10

 56: LOAD_VAR
      Destino: t55
      Arg1: y

 57: LOAD_CONST
      Destino: t56
      Arg1: 3

 58: LOAD_VAR
      Destino: t57
      Arg1: z

 59: LOAD_VAR
      Destino: t58
      Arg1: x

 60: LOAD_VAR
      Destino: t59
      Arg1: y

 61: LOAD_VAR
      Destino: t60
      Arg1: z

 62: LOAD_VAR
      Destino: t61
      Arg1: Opera

 63: LOAD_VAR
      Destino: t62
      Arg1: es

 64: LOAD_VAR
      Destino: t63
      Arg1: de

 65: LOAD_VAR
      Destino: t64
      Arg1: compara

 66: LOAD_VAR
      Destino: t65
      Arg1: o

 67: LOAD_VAR
      Destino: t66
      Arg1: x

 68: LOAD_VAR
      Destino: t67
      Arg1: y

 69: LOAD_CONST
      Destino: t68
      Arg1: "x é igual a y"

 70: LOAD_CONST
      Destino: t69
      Arg1: "x é diferente de y"


CÓDIGO ASSEMBLY ARMv7 (CPUlator):
--------------------------------------------------
.section .data
str_0: .asciz "a é maior que b"
str_1: .asciz "b é maior ou igual a a"
str_2: .asciz "x é igual a y"
str_3: .asciz "x é diferente de y"

.section .text
.global _start
_start:
    push {fp, lr}
    mov fp, sp
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #5
    mov r0, #0
    mov r0, #10
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    ldr r0, =str_0
    ldr r0, =str_1
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #5
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #1
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #3
    mov r0, #0
    mov r0, #0
    mov r0, #1
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #10
    mov r0, #0
    mov r0, #3
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    mov r0, #0
    ldr r0, =str_2
    ldr r0, =str_3
    mov sp, fp
    pop {fp, lr}
    mov r7, #1
    mov r0, #0
    svc #0
--------------------------------------------------

