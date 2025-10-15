# Testing process description

## Algorithm

1. Environment is set up (environment variables, common files).

2. Solution is placed in the filesystem.

3. Precompile checkers are run in order of declaration.
    
    If at least one fails, solution scores 0 points.

4. Solution is compiled.

    If it compiles for too long, it scores 0 points with [CE](./verdicts.md).

    If it fails to compile, it scores 0 points with [CE](./verdicts.md).

5. For each test group, 
    1. If one of dependencies failed, do not run.

    2. For each test case,
      
         1. Place specified in test case files
    
         2. Run solution
       
            If a solution has been running for too long, test case ends with [TL](./verdicts.md).

            If a solution has been taking too much RAM, test case ends with [ML](./verdicts.md).   

         3. Retrieve required output files
            
            If a required file is not present, test case ends with [PE](./verdicts.md).
         
         4. Run all validators.
       
            If at least one fails, test case ends with [WA](./verdicts.md).
       
            If all pass, test case ends with [OK](./verdicts.md).
         
         5. Cleanup files
    
    3. Determine how many points to score based on defined scoring policy for group.

6. Determine final score (sum of all group scores) and verdict (first non-OK verdict).

## Used definitions

{{ decorated_definition("Test suite") }}

{{ decorated_definition("Precompile checker") }}

{{ decorated_definition("Test group") }}

{{ decorated_definition("Test group dependency") }}

{{ decorated_definition("Scoring policy") }}

{{ decorated_definition("Test case") }}

{{ decorated_definition("Test case validator") }}

{{ decorated_definition("Verdict") }}

{{ decorated_definition("Points") }}
