## Example outputs:

Node:
{
	"type": "CLASS" | "OR" | "AND" | "TEXT",
	"data": \[\] (for all but classes),
	"dept": *string* (for classes only),
	"coid": *number* (for classes only),
	"nots": *string* (used for side-notes in parentheses),
}

**Prerequisites: ARCH 2370 Energy, Comfort and Ecology. Corequisites: PHYS 1500, ARCH 2830.**

```
{
	"prereqs": {
		"type": "CLASS",
		"dept": "ARCH",
		"coid": 2370
	},
	"coreqs": {
		"type": "AND",
		"data": [
			{
				"type": "CLASS",
				"dept": "PHYS",
				"coid": 1500
			},
			{
		    "type": "CLASS",
		    "dept": "ARCH",
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
				"dept": "ARTS",
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
						"dept": "BIOL",
						"coid": 1010
					},
					{
						"type": "CLASS",
						"dept": "BIOL",
						"coid": 2120
					},
					{
						"type": "CLASS",
						"dept": "BIOL",
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