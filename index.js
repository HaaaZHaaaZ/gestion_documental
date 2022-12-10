var app = new Vue({
  el: "#app",
  data: {
    message: "",
    info: [],
  },
  mounted() {
    axios.get("http://127.0.0.1:8000/").then((respuesta) => (this.info = respuesta.data));
  },
});

function createPost() {
  let namedocument, tipodocument, areadocument, fechadocument;
  namedocument = document.getElementById("namedocument").value;
  tipodocument = document.getElementById("tipodocument").value;
  areadocument = document.getElementById("areadocument").value;
  fechadocument = document.getElementById("fechadocument").value;
  const toastLiveExample = document.getElementById("liveToast");
  const toast = new bootstrap.Toast(toastLiveExample);
  const config = {
    Nombre: namedocument,
    Tipo: tipodocument,
    Area: areadocument,
    Fecha: fechadocument,
  };

  // axios.post("http://127.0.0.1:8000/",documentos)
  axios
    .post("http://127.0.0.1:8000/", config)
    .then((response) => {
      console.log("post success");
      console.log(response);
      $("editar").modal("hide");

      toast.show();
    })
    .catch((error) => {
      console.log("Oh No! Error!");
      console.log(error);
    });

  console.log(config);
}

function eliminar(element) {
  console.log(element.id);
  axios
    .delete("http://127.0.0.1:8000/" + element.id)
    .then((response) => {
      location.reload();
      console.log(response);
      console.log("Delete success");
    })
    .catch((error) => {
      console.log("Oh No! Error!");
      console.log(error);
    });
}

// function actualizar(element) {
//   console.log(element.id);
//   axios.get("http://127.0.0.1:8000/" + element.id).then(respuesta);
//   console.log(respuesta.data);
// }

let respuesta;

function cargaractualizar(element) {
  respuesta = axios
    .get("http://127.0.0.1:8000/" + element.id)
    .then(
      (respuesta) => (
        (this.info = respuesta.data),
        console.log(info),
        (document.getElementById("iddocumentupdate").value = info._id),
        (document.getElementById("namedocumentupdate").value = info.Nombre),
        (document.getElementById("tipodocumentupdate").value = info.Tipo),
        (document.getElementById("areadocumentupdate").value = info.Area),
        (document.getElementById("fechadocumentupdate").value = info.Fecha)
      )
    );
  return respuesta;
}
console.log(respuesta);

function actualizar() {
  iddocument = document.getElementById("iddocumentupdate").value;
  namedocument = document.getElementById("namedocumentupdate").value;
  tipodocument = document.getElementById("tipodocumentupdate").value;
  areadocument = document.getElementById("areadocumentupdate").value;
  fechadocument = document.getElementById("fechadocumentupdate").value;

  const config = {
    Nombre: namedocument,
    Tipo: tipodocument,
    Area: areadocument,
    Fecha: fechadocument,
  };
  axios
    .put("http://127.0.0.1:8000/" + iddocument, config)
    .then((response) => {
      console.log(response);
      console.log("Updated success");
    })
    .catch((error) => {
      console.log("Oh No! Error!");
      console.log(error);
    });
}
