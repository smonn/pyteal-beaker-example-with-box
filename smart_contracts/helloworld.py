import beaker as bk
import beaker.lib.storage as storage
import pyteal as pt


class HelloWorldState:
    my_box = storage.BoxMapping(key_type=pt.abi.Address, value_type=pt.abi.String)


app = (
    bk.Application("HelloWorldApp", state=HelloWorldState)
    # .apply(deploy_time_immutability_control)
    # .apply(deploy_time_permanence_control)
)


@app.external
def hello(name: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    return pt.Seq(app.state.my_box[pt.Bytes("name")].set(name), output.set(pt.Concat(pt.Bytes("Hello, "), name.get())))
