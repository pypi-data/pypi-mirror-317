

# Class: FederatedObject



URI: [fedid:FederatedObject](https://w3id.org/byon/fedid/v1.0/#FederatedObject)




```mermaid
 classDiagram
    class FederatedObject
      JsonLDObject <|-- FederatedObject
      
      FederatedObject : belongsToDomain
        
      FederatedObject : hasComment
        
      FederatedObject : hasDescription
        
      FederatedObject : hasFederatedId
        
          FederatedObject --> FederatedId : hasFederatedId
        
      FederatedObject : hasLabel
        
      FederatedObject : hasTitle
        
      FederatedObject : id
        
      
```





## Inheritance
* [JsonLDObject](JsonLDObject.md)
    * **FederatedObject**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [hasFederatedId](hasFederatedId.md) | 0..* <br/> [FederatedId](FederatedId.md) |  | direct |
| [belongsToDomain](belongsToDomain.md) | 1..1 <br/> [String](String.md) |  | direct |
| [id](id.md) | 1..1 <br/> [String](String.md) |  | [JsonLDObject](JsonLDObject.md) |
| [hasLabel](hasLabel.md) | 0..* <br/> [String](String.md) |  | [JsonLDObject](JsonLDObject.md) |
| [hasDescription](hasDescription.md) | 0..* <br/> [String](String.md) |  | [JsonLDObject](JsonLDObject.md) |
| [hasComment](hasComment.md) | 0..* <br/> [String](String.md) |  | [JsonLDObject](JsonLDObject.md) |
| [hasTitle](hasTitle.md) | 0..* <br/> [String](String.md) |  | [JsonLDObject](JsonLDObject.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/byon/fedid/v1.0/





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | fedid:FederatedObject |
| native | fedid:FederatedObject |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: FederatedObject
from_schema: https://w3id.org/byon/fedid/v1.0/
is_a: JsonLDObject
slots:
- hasFederatedId
- belongsToDomain
class_uri: fedid:FederatedObject

```
</details>

### Induced

<details>
```yaml
name: FederatedObject
from_schema: https://w3id.org/byon/fedid/v1.0/
is_a: JsonLDObject
attributes:
  hasFederatedId:
    name: hasFederatedId
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: fedid:hasFederatedId
    multivalued: true
    alias: hasFederatedId
    owner: FederatedObject
    domain_of:
    - FederatedObject
    range: FederatedId
  belongsToDomain:
    name: belongsToDomain
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: fedid:belongsToDomain
    multivalued: false
    alias: belongsToDomain
    owner: FederatedObject
    domain_of:
    - FederatedObject
    - DomainIdentifier
    range: string
    required: true
  id:
    name: id
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: jsonld:id
    identifier: true
    alias: id
    owner: FederatedObject
    domain_of:
    - JsonLDObject
    range: string
    required: true
  hasLabel:
    name: hasLabel
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: rdfs:label
    multivalued: true
    alias: hasLabel
    owner: FederatedObject
    domain_of:
    - JsonLDObject
    range: string
  hasDescription:
    name: hasDescription
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: dc:description
    multivalued: true
    alias: hasDescription
    owner: FederatedObject
    domain_of:
    - JsonLDObject
    range: string
  hasComment:
    name: hasComment
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: rdfs:comment
    multivalued: true
    alias: hasComment
    owner: FederatedObject
    domain_of:
    - JsonLDObject
    range: string
  hasTitle:
    name: hasTitle
    from_schema: https://w3id.org/byon/fedid/v1.0/
    rank: 1000
    slot_uri: dc:title
    multivalued: true
    alias: hasTitle
    owner: FederatedObject
    domain_of:
    - JsonLDObject
    range: string
class_uri: fedid:FederatedObject

```
</details>