# UniContract

**UniContract** is a tool designed to simplify multi-language integration by providing a shared interface contract. It generates platform-specific code from a single interface definition, ensuring consistency, flexibility, and scalability across different systems.

## Features

- **Cross-Language Support**: Easily integrate systems written in different programming languages.
- **Unified Interface**: Generate consistent code from a single interface definition.
- **Scalability**: Ideal for large-scale, multi-language projects.
- **Redundancy-Free**: Eliminates the need to define interfaces multiple times.
- **Ease of Maintenance**: Promotes simpler, more maintainable code.

## Purpose and Usage

The primary use case for **UniContract** is to establish a unified interface design, independent of the programming language used for implementation. This project does **not** solve cross-platform communication between programming languages but instead focuses on ensuring consistency in a multi-language environment. 

For example, in a microservice architecture where multiple languages are employed, **UniContract** helps ensure that solutions remain uniform. Developers switching from one programming language to another within the same project will encounter familiar functionality and design patterns, making transitions seamless. Learning the behavior of a specific interface in one language enables developers to predict its behavior in another.

By providing a single source of truth for interface definitions, UniContract reduces development overhead and potential discrepancies that arise from manually maintaining multiple definitions across different platforms. This consistency fosters better collaboration among developers and improves the overall reliability of multi-language systems.

### Practical Example

One of the best examples of this approach is an interface for database operations. Imagine a unified interface for storing, modifying, and retrieving entities, which works the same regardless of the underlying language. For instance, whether working in Java, Python, or C#, the interface behaves predictably, and the expected functionality remains consistent. This enables developers to work efficiently across different services and programming languages without steep learning curves.

For example, an interface like `DataStore` could define methods for basic CRUD operations:

- **Create**: Adding a new entity to the database.
- **Read**: Retrieving data based on specific conditions.
- **Update**: Modifying existing data.
- **Delete**: Removing data.

With UniContract, the same `DataStore` interface can be generated in multiple programming languages, ensuring that developers always interact with familiar constructs.

## Related Projects

UniContract is part of the **MicronIQ** project, a broader initiative to create consistent, language-agnostic patterns for microservices. One key implementation of UniContract can be found in the **PolyPersist** project, which leverages this tool to provide a unified interface for database operations. Check out the PolyPersist project here:

[PolyPersist on GitHub](https://github.com/gyorgy-gulyas/PolyPersist)

## Installation and Usage

```bash
# Clone the repository
git clone https://github.com/your-username/unicontract.git

# Navigate into the directory
cd unicontract

# Follow setup instructions based on your environment
# Example: Run installation script or configure dependencies

# Example Interface Definition (user-service.contract)
#
# interface UserService {
#   method getUser(userId: string) -> User
# }
#
# interface User {
#   property id: string
#   property name: string
# }

# To generate code for multiple languages from the interface definition:
unicontract --input user-service.contract --emitter ./emmitters/java.py -emitter ./emmitters/python.py -emitter ./emmitters/dotnet.py

# This will generate the necessary code files for the UserService interface
# in Java, Python, and C#.
```
