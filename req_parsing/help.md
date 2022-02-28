Lexing tokens:
- DELIMITERS: [:;.,]
- CLASSES: "ARCH 1011", "BIOL 1015", "CSCI 1200"
	* PSYC 1200
	* ISYE 4760 (MATP)
	* ISYE 4760 (MATP 4620)
	* ENGR-2600
	* linear algebra and programming (e.g., MATH-1020 and CSCI-1010 or CSCI-1100)
	* ERTH 1200 Geology II
	* Database Systems (CSCI 4380)
	* Data Science (CSCI/ERTH/ITWS 496x/696x)
	* PSYC/PHIL 2120
	* ARCH 6910 Doctoral Seminar 1
- LOGICAL OPERATORS: "except", "or", "and", "/"
- TEXT: "familiarity with probability", "permission of instructor"
- SIDETEXT: "(or higher)"

# Example outputs:

Node:
{
	"type": "CLASS" | "OR" | "AND" | "TEXT",
	"data": \[\] (for all but classes),
	"dpmt": *string* (for classes only),
	"coid": *number* (for classes only),
	"nots": *string* (used for side-notes in parentheses),
}

**Prerequisites: ARCH 2370 Energy, Comfort and Ecology. Corequisites: PHYS 1500, ARCH 2830.**

```
{
	"prereqs": {
		"type": "CLASS",
		"dpmt": "ARCH",
		"coid": 2370
	},
	"coreqs": {
		"type": "AND",
		"data": [
			{
				"type": "CLASS",
				"dpmt": "PHYS",
				"coid": 1500
			},
			{
		    "type": "CLASS",
		    "dpmt": "ARCH",
		    "coid": 2830,	
			}
		]
	}
}
```

**Prerequisite: ARTS 2230 or permission of instructor.**

```
{
	"prereqs": {
		"type": "OR",
		"data": [
			{
				"type": "CLASS",
				"dpmt": "ARTS",
				"coid": 2230
			},
			{
				"type": "TEXT",
				"data": "permission of instructor"
			}
		]
	},
	"coreqs": {}
}
```

**Restricted to Biology majors who have completed BIOL 1010, BIOL 2120, and BIOL 2500, or equivalents and who have permission of the instructor to register.**

```
{
	"prereqs": {
		"type": "OR",
		"data": [
			{
				"type": "AND",
				"data: [
					{
						"type": "text",
						"data": "Restricted to Biology majors"
					},
					{
						"type": "CLASS",
						"dpmt": "BIOL",
						"coid": 1010
					},
					{
						"type": "CLASS",
						"dpmt": "BIOL",
						"coid": 2120
					},
					{
						"type": "CLASS",
						"dpmt": "BIOL",
						"coid": 2500
					}
				]
			},
			{
				"type": "text",
				"data": "equivalents and who have permission of the instructor to register"
			}
		]
	},
	"coreqs": {}
}
```