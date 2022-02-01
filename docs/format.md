# Data Documentation

The data for CRISIS are stored as a dictionary, where each key is a combination of a course's department and course number, in the form: `'DEPT-CRSE'`. A keys corresponding value is an object which holds several properties about the course.

## Properties

| Property | Description | Example |
|-|-|-|
| `"title"`       | Course name. | `"CALCULUS I"` |
| `"crns"`        | List of CRNs from this course's sections. | `[61326, 60309,...]` |
| `"department"`  | Department code. | `"MATH"` |
| `"id_num"`      | Course code. | `1010` |
| `"credits"`     | Number of credits for the course. May be a range of values. | `"4.0"`, or `"1.0-4.0"` |
| `"ci"`          | Whether this course is **c**ommunication **i**ntensive. | `false` |
| `"description"` | Course description. | `"Functions, limits, continuity, derivatives, implicit..."` |
| `"offered"`     | When the course can be taken. | `"Fall and spring terms annually."` |
| `"prereq"`      | List of prerequisite courses. | `["MATH 1000", "MATH 1001"]` |
| `"coreq"`       | List of corequisite courses. | `["MATH 1002", "MATH 1003"]` |
| `"cross"`       | List of cross-listed classes. | `["CSCI 0123", "PSYC 4567"]` |
| `"required_by"` | Contains course requirements for major, minor, etc.
| |`"minor"` List of minors which require this course. | `["MATH", "GSAS"]` |
| |`"major"` List of majors which require this course. | `["CSCI", "COGS"]` |
| | `"hass"` List of HASS pathways that require this course. | `["Artificial Intelligence", "Mind, Brain, and Intelligence"]` |
| `"transfer"` | A list of courses which can be redeemed when transferring to RPI. | |
| | `"school"` Name of the college. | `"Univ Texas Austin"` |
| | `"location"` Location of the college. | `"Texas"` |
| | `"title"` Title of course at the college. | `"INTRODUCTION TO PSYCHOLOGY"` |
| | `"id"` Course ID or code. | `"PSY 301"` |

## Example Template
```
"MATH-1010": {
  "title": "CALCULUS I",
  "department": "MATH",
  "id_num": 1010,
  "credits": "4.0",
  "ci": false,
  "description": "Functions, limits, continuity, derivatives, implicit differentiation, related rates, maxima and minima, elementary transcendental functions, introduction to definite integral with applications to area and volumes of revolution.",
  "offered": "Fall and spring terms annually.",
  "prereq": [
    "MATH 1000",
    "MATH 1001"
  ],
  "coreq": [
    "MATH 1002",
    "MATH 1003"
  ],
  "cross": [
    "CSCI 0123",
    "PSYC 4567"
  ],
  "required-by": {
    "major": [
      "MATH",
      "GSAS"
    ],
    "minor": [
      "CSCI",
      "COGS"
    ],
    "hass": []
  },
  "transfer": [
    {
      "school": "Univ of Connecticut",
      "location": "Connecticut",
      "title": "CALCULUS I",
      "id": "MATH 1131Q"
    },
    {
      "school": "Univ Of New Haven",
      "location": "Connecticut",
      "title": "CALCULUS I",
      "id": "M 117"
    }
  ]
}
```

## Blank Template
```
"NULL-0000": {
  "title": "",
  "department": "",
  "id_num": 0000,
  "credits": "0.0",
  "ci": false,
  "description": "",
  "offered": "",
  "prereq": [],
  "coreq": [],
  "cross": [],
  "required-by": {
    "major": [],
    "minor": [],
    "hass": []
  },
  "transfer": []
}
```
