NEOMODEL_TEMPLATE = """
class FollowRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)

class SubscribeRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)

class ReadRel(StructuredRel):
    read_time = DateTimeProperty(default_now=True, index=True)

class SaveRel(StructuredRel):
    save_time = DateTimeProperty(default_now=True, index=True)

class Entity(StructuredNode):
    name = StringProperty(unique_index=True)

    follows = RelationshipTo("Entity", "follow", model=FollowRel)
    followers = RelationshipFrom("Entity", "follow", model=FollowRel)
    # all papers that an entity has already read, a known list
    reads = RelationshipTo("Paper", "read", model=ReadRel)
    # all papers that an entity is going to read, a reading list
    lists = RelationshipTo("Paper", "save", model=SaveRel)
    subscriptions = RelationshipTo("Venue", "subscribe", model=SubscribeRel)

class Paper(StructuredNode):
    paper_id = StringProperty(unique_index=True)
    arxiv_id = StringProperty()
    title = StringProperty()
    abstract = StringProperty()
    summary = StringProperty()
    publication_date = DateTimeProperty()
    reference_count = IntegerProperty()
    citation_count = IntegerProperty()
    pdf = StringProperty()
    # openai text-embedding-3-large cast to 1024
    embedding_te3l = ArrayProperty(FloatProperty())

    references = RelationshipTo("Paper", "cite")
    citations = RelationshipFrom("Paper", "cite")
    readers = RelationshipFrom("Entity", "read", model=ReadRel)

class Collection(StructuredNode):
    # it is used to hold the particular collection of a venue
    # for example: ICLR22, CVPR24
    name = StringProperty(unique_index=True)

    papers = RelationshipTo("Paper", "contain")


class Venue(StructuredNode)
    # it is used to hold the information of conference / journal
    # for example: ICLR, CVPR, Science, Nature
    name = StringProperty(unique_index=True)

    collections = RelationshipTo("Collection", "publish")

Besides, there is a vector index set on Paper.embedding_te3l, you can use
this index to do semantic search if necessary.

sample usage:
1. Suppose you want to find some paper about query: LLM, and you want to retrieve 10 papers
```cypher
call db.index.vector.queryNodes('vector_embedding_te3l', 10, $embeddings)
YIELD node AS paper

RETURN paper
```

2. Suppose you want to find some paper from a specified paper, and you want to retrieve 3 papers
```cypher
MATCH (p0:Paper) WHERE ... # SOME MATCH CONDITION
CALL db.index.vector.queryNodes('vector_embedding_te3l', 3, p0.embedding_te3l)
YIELD node AS paper

RETURN paper
```

**NOTICE**
1. If you need to retrieve paper, please ONLY return
[title, paper_id, publication_date, citation_count, reference_count, pdf]

2. Always use *LIMIT* at the end of cypher query to restrict the number of results under 20.

3. Always translate publication date into a readable format.
"""
