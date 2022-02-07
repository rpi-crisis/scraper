(ns org.rpicrisis.scraper.catalog
  (:require [clojure.edn :as edn]
            [clojure.spec.alpha :as s]
            [clojure.string :as str]
            [hickory.core :refer [parse as-hickory]]
            [hickory.select :as sel]
            [org.rpicrisis.scraper.data :refer :all]))


(defn subject-url [subject]
  (str "http://catalog.rpi.edu/content.php?navoid=544&filter[27]="
       (subject->str subject)))

(defn coid-url [coid]
  (str "http://catalog.rpi.edu/preview_course_nopop.php?catoid=22&coid="
       coid))

(defn fetch [url]
  (as-hickory (parse (slurp url))))

(defn comm-intensive? [desc]
  (str/ends-with? desc "This is a communication-intensive course."))

(def course-selector
  (sel/descendant (sel/class :block_content)
                  (sel/not (sel/tag :br))))

(defn cleanup-course [html]
  (->> (sel/select course-selector html)
       (filter string?)
       (remove str/blank?)
       (drop 7)
       (take-while #(not= % " "))))

(defn fetch-course [coid]
  (let [url (coid-url coid)
        html (fetch url)
        strs (cleanup-course html)
        desc (first strs)
        meta (apply hash-map (map str/triml (rest strs)))]
    {:description desc
     :prereqs (meta "Prerequisites/Corequisites:")
     :credits (edn/read-string (meta "Credit Hours:"))
     :offered (meta "When Offered:")
     :cross (meta "Cross Listed:")}))

(def subject-course-selector
  (sel/attr :href #(str/starts-with? % "preview_course_nopop.php")))

(defn parse-course-from-subject [elem]
  (let [coid (second (re-find #"coid=(\d+)" (get-in elem [:attrs :href])))
        [_ subject code title] (re-find #"([A-Z]{4}) (\d{4}) - (.*)" (get-in elem [:content 0]))]
    {:coid coid
     :subject (str->subject subject)
     :code code
     :title title}))

(defn fetch-subject [subject]
  {:pre [(s/valid? :org.rpicrisis.scraper.data/subject subject)]}
  (let [url (subject-url subject)
        html (fetch url)
        elems (sel/select subject-course-selector html)
        courses (take 15 (map parse-course-from-subject elems))]
    (map #(dissoc (merge % (fetch-course (:coid %))) :coid) courses)))
