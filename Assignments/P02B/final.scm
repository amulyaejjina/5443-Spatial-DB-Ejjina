
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

; Function to find the sum of divisors
(define (findSum m n sum)
  ; Base case
  (if (= n 0)
      sum
      ; Implied else for non-base case
      ; Return facTail(n-1, n*tot)
      (if (integer? (/ m (- n 1)))
        (findSum m (- n 1) (+ sum (- n 1)))
        (findSum m (- n 1) sum))))


; Function to classify based on
; sum of divisors
(define (classify n result)
(print "The sum of proper divisors is : " result)
; comapre the sum and number to decide
; whether its perfect/abundant/deficient
(cond
      [( = result n) "Classification : Perfect number !!!"]
      [( > result n) "Classification : Abundant number "]
      [( < result n) "Classification : Deficient number"]))


;The below is to output the program description and comments to terminal
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

(print "Please enter a number :")
(define n (read))
; Function call and saving the 
; result of it in a variable named "result"
(define result (findSum n (+ (ceiling (/ n 2)) 1) 0))
; Function call to classify the number
; based on result
(classify n result)

; -----------------------------    End of Program    -----------------------------