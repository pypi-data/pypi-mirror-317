from pyorient.ogm import declarative
from pyorient.ogm import property

Node = declarative.declarative_node()
Relationship = declarative.declarative_relationship()


class GraphVertexBase(Node):
    value = property.String(nullable=False)
    category = property.String(nullable=False)
    type = property.String(nullable=False)


class EntityRoot(GraphVertexBase):
    entity_id = property.String(nullable=False, indexed=True)

    element_plural = "entity_root"


class Asset(GraphVertexBase):
    asset_id = property.String(nullable=False)
    host_name = property.String(indexed=True)
    primary_ip = property.String(indexed=True)

    element_plural = "asset"


class OS(GraphVertexBase):
    os_type = property.String()
    full = property.String()
    distribution = property.String()
    kernel_version = property.String()
    build_version = property.String()
    bitness = property.Short()

    element_plural = "os"


class IP(GraphVertexBase):
    addr = property.String(indexed=True)
    mac = property.String()
    exposure = property.Byte(indexed=True)

    element_plural = "ip"


class Port(GraphVertexBase):
    number = property.Integer(indexed=True)
    protocol = property.String()
    banner = property.String()
    exposure = property.Byte(indexed=True)

    element_plural = "port"


class Owner(GraphVertexBase):
    name = property.String()

    element_plural = "owner"


class Email(GraphVertexBase):
    email = property.String()

    element_plural = "email"


class Phone(GraphVertexBase):
    phone = property.String()

    element_plural = "phone"


class Department(GraphVertexBase):
    name = property.String()

    element_plural = "department"


class Realm(GraphVertexBase):
    name = property.String()

    element_plural = "realm"


class Vul(GraphVertexBase):
    name = property.String()
    cve_id = property.String()
    cvss_score = property.Float()
    description = property.String()
    solution = property.String()
    message = property.String()
    vul_id = property.String()

    element_plural = "vul"


class Component(GraphVertexBase):
    name = property.String()
    version = property.String()

    element_plural = "component"


class Account(GraphVertexBase):
    name = property.String()
    home = property.String()
    shell = property.String()
    root = property.Boolean()
    sudo = property.Boolean()
    expired = property.Boolean()
    login_type = property.Byte()
    interactive_login_type = property.Integer()
    login_status = property.Integer()

    element_plural = "account"


class Group(GraphVertexBase):
    name = property.String()

    element_plural = "group"


class Process(GraphVertexBase):
    name = property.String()
    pname = property.String()
    string = property.String()
    path = property.String()

    element_plural = "process"


class WebServer(GraphVertexBase):
    server = property.String()
    protocol = property.String()
    cmd = property.String()

    element_plural = "webserver"


class WebSite(GraphVertexBase):
    name = property.String()
    title = property.String()

    element_plural = "website"


class WebFrame(GraphVertexBase):
    name = property.String()
    version = property.String()
    lang = property.String()

    element_plural = "webframe"


class DB(GraphVertexBase):
    name = property.String()
    version = property.String()
    data_dir = property.String()

    element_plural = "db"


class InternetPort(GraphVertexBase):
    ip = property.String()
    port = property.Integer()

    element_plural = "internet_port"


class Relation(Relationship):
    relation = property.String()

    label = "relation"
