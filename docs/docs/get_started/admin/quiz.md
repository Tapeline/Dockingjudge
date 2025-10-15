# Quiz tasks

![](../../img/ui-edit-quiz.png)

## How to create a quiz task

1. Press a button for adding a quiz task in **Settings**
2. Write a name and a statement
3. Write a [checker declaration](../../reference/checking/quiz.md)
4. Determine, how many points will user score for submitting a correct answer

## Example data

- Name: `Math test 1`
- Statemtent:
  ``` markdown
  What's $2 + 2 * 2$?
  ```
- Checker:
  ``` json
  {
    "args": {
      "pattern": "6"
    },
    "type": "text"
  }
  ```
- Points: `100`

> Learn more: 
> 
> - [Reference > Quiz page](../../reference/pages/quiz.md)
> - [Reference > Quiz solutions](../../reference/solutions/quiz.md)
> - [Reference > Quiz validators](../../reference/checking/quiz.md)

