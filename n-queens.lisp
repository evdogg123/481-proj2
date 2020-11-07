(in-package :cl-user)
(defpackage :n-queens
  (:documentation "Requires alexandria.  If you want to get JSON
output, also requires jonathan.")
  (:use :cl)
  (:export :solutionp
           :generate-variables
           :generate-csp
           :to-json))

(in-package :n-queens)


(defun solutionp (assignment)
  "True iff ASSIGNMENT is a solution (that is, ASSIGNMENT is complete
and consistent) to the n-queens problem."
  ;; Here we just do a n^2 loop through the queens and make sure that
  ;; for each pair that they're not attacking each other horizontally
  ;; or along either of the diagonals.
  (loop for i from 1 to (length assignment) do
    (loop for j from (1+ i) to (length assignment) do
      (let ((pos-i (cadr (assoc (intern (format nil "Q~A" i) :keyword) assignment)))
            (pos-j (cadr (assoc (intern (format nil "Q~A" j) :keyword) assignment))))
        (when (or (= pos-i pos-j)
                  (= pos-j (+ pos-i (- j i)))
                  (= pos-j (- pos-i (- j i))))
          (return-from solutionp nil)))))
  t)


(defun generate-constraints (num-queens)
  ;; This the part that would be awful to do by hand - generate, for
  ;; each pair of queens, all the possible compatible assignments for
  ;; those two queens.
  (loop for i from 1 to num-queens nconc
    (loop for j from (1+ i) to num-queens collect
      (cons (list (intern (format nil "Q~A" i) :keyword)
                  (intern (format nil "Q~A" j) :keyword))
            (remove-if #'(lambda (pair)
                           (or (= (car pair) (cadr pair))
                               (= (cadr pair) (+ (car pair) (- j i)))
                               (= (cadr pair) (- (car pair) (- j i)))))
                       (alexandria:map-product #'list
                                               (loop for x from 1 to num-queens collect x)
                                               (loop for x from 1 to num-queens collect x)))))))


(defun generate-variables (num-queens)
  "Generate the queen/domain a-list for NUM-QUEENS queens.  This will
give the full domains - e.g. for each queen q,
(cdr (assoc q (generate-variables 8))) will be (1 2 3 4 5 6 7 8)."
  (mapcar #'(lambda (queen)
              (cons queen (loop for i from 1 to num-queens collect i)))
          (loop for j from 1 to num-queens collect (intern (format nil "Q~A" j) :keyword))))


(defun generate-csp (num-queens)
  "Generate a constraint satisfaction problem of size NUM-QUEENS,
where each queen's domain is all NUM-QUEES rows.  The queen variables
and domains are specified as a-lists, and the constraints are lists of
pairs where the first pair is the two queens involved in the
constraint, and the rest of the pairs represent all the compatible
assignments between those two queens."
  (list :variables (generate-variables num-queens)
        :constraints (generate-constraints num-queens)))


(defun to-json (csp)
  "Gives a JSON representation of CSP.  The variables a-lists are
turned into a dictionary where the keys are queens and the values are
the domains.  The constraints remain as lists of pairs.

An example usage to dump the 8 queens representation to a file called
8-queens-csp.json in Flimby's home directory on a Mac:

(with-open-file (out #P\"/Users/flimby/8-queens-csp.json\" :direction :output)
  (format out (n-queens:to-json (n-queens:generate-csp 8))))"
  (let ((json-data (make-hash-table :test #'equal)))
    (setf (gethash "variables" json-data)
          (make-hash-table :test #'equal))
    (dolist (var (getf csp :variables))
      (setf (gethash (symbol-name (car var))
                     (gethash "variables" json-data))
            (make-array (1- (length var)) :initial-contents (cdr var))))
    (setf (gethash "constraints" json-data)
          (make-array (length (getf csp :constraints))
                      :initial-contents (mapcar #'(lambda (constraint)
                                                    (make-array (length constraint)
                                                                :initial-contents (mapcar #'(lambda (x)
                                                                                              (make-array 2 :initial-contents x))
                                                                                          constraint)))
                                                (getf csp :constraints))))
    (jonathan.encode:to-json json-data)))
