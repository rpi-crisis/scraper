(ns org.rpicrisis.scraper.data
  (:require [clojure.edn :as edn]
            [clojure.string :as str]
            [clojure.spec.alpha :as s]))
(def schools
  (edn/read-string (slurp "data/schools.edn")))

(def subjects
  (edn/read-string (slurp "data/subjects.edn")))

(def subjects-set
  (set (mapcat keys (vals subjects))))

(s/def ::subject subjects-set)

(s/def ::course-code (s/int-in 1000 10000))

(s/def ::course (s/cat :subject ::subject
                       :code ::course-code))

(defn subject->str [subject]
  {:pre [(s/valid? ::subject subject)]
   :post [(string? %)]}
  (str/upper-case (name subject)))

(defn str->subject [s]
  {:pre [(string? s)]
   :post [(s/valid? ::subject %)]}
  (keyword (str/lower-case s)))

(defn course->str [course]
  {:pre [(s/valid? ::course course)]
   :post [(string? %)]}
  (str (subject->str (first course)) "-" (second course)))

(defn str->course [s]
  {:pre [(string? s)]
   :post [(s/valid? ::course %)]}
  (let [[subject code] (str/split s #"-" 2)]
    [(str->subject subject) (edn/read-string code)]))
