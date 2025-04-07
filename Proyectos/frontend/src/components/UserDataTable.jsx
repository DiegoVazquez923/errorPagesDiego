import React, { useState, useEffect } from "react";
import DataTable from "react-data-table-component";
import { Modal, Button, Form } from 'react-bootstrap';
import Swal from 'sweetalert2'
import { tokenRefresh } from "../services/authService";

const UserDataTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [usuarioSel, setUsuarioSel] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const email = localStorage.getItem("email");

  const url = "http://127.0.0.1:8000/users/api/";
  const userId = localStorage.getItem("userId");

  const openModal = (user) => {
    setUsuarioSel(user);
    setShowModal(true);
  };

  const closeModal = () => {
    setUsuarioSel(null);
    setShowModal(false);
  };

  const getData = async () => {
    try {
      const response = await tokenRefresh.get(url);
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error al cargar los datos:", error);
    }
  };

  useEffect(() => {
    getData();
  }, []);


  const actualizarUser = () => {
    Swal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas actualizar este usuario?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Actualizar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        tokenRefresh
          .put(`${url}${usuarioSel.id}/`, usuarioSel)
          .then(() => {
            getData();
            closeModal();
            Swal.fire({
              title: "Usuario actualizado",
              text: "El usuario ha sido actualizado correctamente",
              icon: "success"
            });
          })
          .catch((error) => {
            console.error(error);
            Swal.fire({
              title: "Error al actualizar",
              text: "Ha ocurrido un error",
              icon: "error"
            });
          });
      }
    });
  };

  const borrarUser = (id) => {
    Swal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas eliminar este usuario?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        tokenRefresh
          .delete(`${url}${id}/`)
          .then(() => {
            getData();
            Swal.fire({
              title: "Usuario eliminado",
              text: "El usuario ha sido eliminado correctamente",
              icon: "success"
            });
          })
          .catch((error) => {
            console.error(error);
            Swal.fire({
              title: "Error al eliminar",
              text: "No se pudo eliminar el usuario",
              icon: "error"
            });
          });
      }
    });
  };

  const columns = [
    {
      name: "Nombre",
      selector: (row) => row.name,
      sortable: true,
    },
    {
      name: "Email",
      selector: (row) => row.email,
      sortable: true,
    },
    {
      name: "Teléfono",
      selector: (row) => row.tel,
    },
    {
      name: "Acciones",
      cell: (row) => (
        <span>
          <button className="btn btn-warning me-2" onClick={() => openModal(row)}>
            <i className="bi bi-pencil"></i>
          </button>
          {parseInt(userId) !== row.id ? (
            <button className="btn btn-danger" onClick={() => borrarUser(row.id)}>
              <i className="bi bi-trash"></i><br />
            </button>
          ) : null}

        </span>
      ),
    },
  ];

  return (
    <div className="container mt-4">
      <h3>Tabla de usuarios</h3>
      <DataTable
        columns={columns}
        data={data}
        progressPending={loading}
        pagination
        highlightOnHover
        pointerOnHover
      />

      {showModal && usuarioSel && (
        <Modal show={showModal} onHide={closeModal} centered>
          <Modal.Header closeButton>
            <Modal.Title>Editar Usuario</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group className="mb-3" controlId="formNombre">
                <Form.Label>Nombre:</Form.Label>
                <Form.Control type="text" value={usuarioSel.name}
                  onChange={(e) => setUsuarioSel({ ...usuarioSel, name: e.target.value })}
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formApellido">
                <Form.Label>Apellido:</Form.Label>
                <Form.Control type="text" value={usuarioSel.surname}
                  onChange={(e) => setUsuarioSel({ ...usuarioSel, surname: e.target.value })}
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Label>Email:</Form.Label>
                <Form.Control type="email" value={usuarioSel.email}
                  onChange={(e) => setUsuarioSel({ ...usuarioSel, email: e.target.value })}
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formTelefono">
                <Form.Label>Teléfono:</Form.Label>
                <Form.Control type="text" value={usuarioSel.tel}
                  onChange={(e) => setUsuarioSel({ ...usuarioSel, tel: e.target.value })}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={closeModal}>
              Cancelar
            </Button>
            <Button variant="primary" onClick={actualizarUser}>
              Guardar cambios
            </Button>
          </Modal.Footer>
        </Modal>
      )}
    </div>
  );
};

export default UserDataTable;
