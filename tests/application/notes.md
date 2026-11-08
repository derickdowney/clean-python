# Application Layer

Application layer creates use cases that orchestrate domain objects while
maintaining clean arhcitectural boundaries.

Using ports, adapters, and request/response models, we create a system where
components can evolve independently yet work together seamlessly.

Distinct resposibilities of the Application layer: (p. 111)
- Use case orchestration
    - Coordinating domain objects to accomplish user tasks
    - Managing the sequence of operations
    - Ensuring business rules are properly applied
- Error handling and validation
    - Validating input before it reaches domain objects
    - Catching and translating domain errors
    - Providing consistent error responses
- Transaction management
    - Ensuring operations are atomic when needed
    - Maintaining data consistency
    - Managing rollback on failures
- Boundary translation
    - Converting external data formats to domain formats
    - Transforming domain objects for external presentation
    - Managing cross-boundary communication

# Expected Errors Only!!!
"When implementing error handling in the Application layer, we explicitly catch
and transform only expected domain and business errors into results. Thus, we
don't have an `except Exception:` clause paired with the expected errors. This
separation maintains clean architectural boundaires. Concerns such as global
error handling remain in the outer layers." p. 114
- TL;DR only look for known domain/business errors at applicaiton level
