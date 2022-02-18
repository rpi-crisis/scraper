# Data Documentation

The data for CRISIS are stored as a json array, where each element is
an object with the following form:

## Course Properties

| Property        | Description                                                 | Example                                                     |
|-----------------|-------------------------------------------------------------|-------------------------------------------------------------|
| `"title"`       | Course name.                                                | `"CALCULUS I"`                                              |
| `"department"`  | Department code.                                            | `"MATH"`                                                    |
| `"id"`          | Course code.                                                | `1010`                                                      |
| `"credits"`     | Number of credits for the course. May be a range of values. | `"4"`, or `"1-4"`                                          |
| `"ci"`          | Whether this course is **c**ommunication **i**ntensive.     | `false`                                                     |
| `"description"` | Course description.                                         | `"Functions, limits, continuity, derivatives, implicit..."` |
| `"offered"`     | When the course can be taken.                               | `"Fall and spring terms annually."`                         |
| `"prereq"`      | (TODO) Free-form string of prerequisite courses.            | `"MATH 1000 and MATH 1001"`                                 |
| `"coreq"`       | (TODO) Free-form string of corequisite courses.             | `"MATH 1002 and MATH 1003"`                                 |
| `"cross"`       | (TODO) Free-form string of cross-listed courses.            | `"CSCI 0123 and PSYC 4567"`                                 |
| `"sections"`    | A list of section objects                                   | See below                                                   |

## Section Properties

| Property      | Description                                         | Example   |
|---------------|-----------------------------------------------------|-----------|
| `"crn"`       | CRN of the section.                                 | `"50039"` |
| `"section"`   | Section number.                                     | `"01"`    |
| `"capacity"`  | Total capacity of the section.                      | `30`      |
| `"enrolled"`  | Number of current students enrolled in the section. | `25`      |
| `"remaining"` | `capacity - enrolled`                               | `5`       |
| `"meetings"`  | List of meeting objects                             | See below |

## Meeting Properties

| Property        | Description                            |                                         |
|-----------------|----------------------------------------|-----------------------------------------|
| `"time"`        | Time table of the meeting.             | `"2:00 pm - 3:20 pm"`                   |
| `"days"`        | Which days the meetings take place on. | `"MR"`                                  |
| `"location"`    | Room number or online status.          | `"Darrin Communications Center 308"`    |
| `"type"`        | Lecture/recitation/exam etc.           | `"Lecture"`                             |
| `"instructors"` | Instructor(s) for the meeting.         | `"Wesley D Turner, Shianne M. Hulbert"` |

## Example Template

```json
{
  "CSCI-1100": {
    "title": "COMPUTER SCIENCE I",
    "department": "CSCI",
    "id": 1100,
    "credits": "4"
    "description": "--description--",
    "prereqs": "--prerequesites--",
    "coreqs": "--corequesites--",
    "crosslistings": "--crosslistings--",
    "sections": [
      {
        "crn": "50039",
        "section": "01",
        "capacity": 30,
        "enrolled": 25,
        "remaining": 5,
        "meetings": [
          {
            "time": "2:00 pm - 3:20 pm",
            "days": "MR",
            "location": "Online ",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          },
          {
            "time": "10:00 am - 11:50 am",
            "days": "T",
            "location": "Low Center for Industrial Inn. 3116",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          },
          {
            "time": "6:00 pm - 7:50 pm",
            "days": "R",
            "location": "Darrin Communications Center 308",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          }
        ]
      },
      {
        "crn": "50373",
        "section": "02",
        "meetings": [
          {
            "time": "2:00 pm - 3:20 pm",
            "days": "MR",
            "location": "Online ",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          },
          {
            "time": "10:00 am - 11:50 am",
            "days": "T",
            "location": "Carnegie Building 208",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          },
          {
            "time": "6:00 pm - 7:50 pm",
            "days": "R",
            "location": "Darrin Communications Center 308",
            "type": "Lecture",
            "instructors": "Wesley D Turner, Shianne M. Hulbert"
          }
        ],
        "capacity": 36,
        "enrolled": 29,
        "remaining": 7
      }
    ]
  }
}
```
