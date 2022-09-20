
;----------------------------------------------------------------------")
;                            PROGRAM 1                                 ")
;  Name        : Amulya Ejjina")
;  Course      : CMPS 5113")
;  Instructor  : Dr.Tina Johnson")
;  Description : This program will classify a passed positive integer")
;                to either Perfect,abundant or deficeint.")
;                A positive integer is perfect number N if sum of it's")
;                proper divisors less than N is equal to N. ")
;                If the sum is greater than N,the number is abundant.")
;                If the sum is less than N,the number is deficient")
;----------------------------------------------------------------------")

(define (fac n)
  ; If n = 1, the base case is reached, return 1
  (if (= n 1)
      1
      ; Implied else for non-base case
      ; Return n * fac(n - 1) 
      (* n (fac (- n 1)))))

; The facTail function uses tail recursion to return n!
(define (facTail n tot)
  ; If n = 1, the base case is reached, return n!
  ; which is stored in tot.  Using tail recursion
  ; tot keeps an accumulated value in each call
  ; to the tail recursive function.
  (if (= n 1)
      tot
      ; Implied else for non-base case
      ; Return facTail(n-1, n*tot)
      (facTail (- n 1)(* n tot))))


;The below is to output the program description and commenst to terminal
(print "----------------------------------------------------------------------")
(print "                            PROGRAM 1                                 ")
(print "Name        : Amulya Ejjina")
(print "Course      : CMPS 5113")
(print "Instructor  : Dr.Tina Johnson")
(print "Description : This program will classify a passed positive integer")
(print "              to either Perfect,abundant or deficeint.")
(print "              A positive integer is perfect number N if sum of it's")
(print "              proper divisors less than N is equal to N. ")
(print "              If the sum is greater than N,the number is abundant.")
(print "              If the sum is less than N,the number is deficient")
(print "----------------------------------------------------------------------")