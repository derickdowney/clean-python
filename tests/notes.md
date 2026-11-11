I asked ChatGPT for feedback on my TDD code. It had the following advice.

# Major Takeaway
- Instantiate objects directly in constructor/init tests
- Use object factory in behavior tests
- A failing testing suite can be good.
    - It can reveal that a fundamental contract has changed.


# Use a Factory when Instantiation Is Not Important
I am doing the following all over: `task: Task = Task("t", "d")`
However, if we add a new required argument to Task, then all of these
tests would fail for reasons different than why the test exists!!!

**"Tests should construct their test subjects through a common factory whenever
the specific construction details aren't relevant to the test."**

"This is sometimes called a Test Data Builder or Object Mother pattern.
You don't need to formally implement either pattern, though.
A simple helper function is perfectly adequate."


# Don't use Factory when Testing Construction!!!
For tests like `test_Task_init_requires...`, do NOT use the factory!!!
When you are specifically testing initialization, then you should
initialize the real way!

**Don't try to prevent all tests from breaking.
Try to prevent unrelated tests from breaking.**


# Add Flexibility to Factory
Allow for defaults, but allow for keyword-arg overrides when needed:
```Python
def create_task(
    *,
    title: str = "title",
    description: str = "description",
    due_date: Deadline | None = None,
    priority: Priority = Priority.MEDIUM,
) -> Task:
    """Creates a valid Task() instance."""
    return Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
    )
```
