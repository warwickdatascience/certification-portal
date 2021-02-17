<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Certificates</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.cert-modal>Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Cert Code</th>
              <th scope="col">Student</th>
              <th scope="col">Student Email</th>
              <th scope="col">Course</th>
              <th scope="col">Mentor</th>
              <th scope="col">Date Issued</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cert, index) in certs" :key="index">
              <td> {{ cert.certification_code }} </td>
              <td> {{ cert.student_name }} </td>
              <td> {{ cert.student_email }} </td>
              <td> {{ cert.course }} </td>
              <td> {{ cert.mentor }} </td>
              <td> {{ cert.date_issued }} </td>
              <td> {{ cert.certification_date }} </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addCertModal"
         id="cert-modal"
         title="Add a new cert"
         hide-footer>
      <b-form class="w-100">
      <b-form-group id="form-title-group"
                    label="Student First Name:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addCertForm.student_fname"
                        required
                        placeholder="ex. John">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Student Last Name:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addCertForm.student_lname"
                          required
                          placeholder="ex. Doe">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-author-group"
                    label="Student Email:"
                    label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addCertForm.student_lname"
                        required
                        placeholder="ex. John.Doe@warwick.ac.uk">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                    label="Course:"
                    label-for="form-course-input">
          <b-form-select
            id="form-course-group"
            v-model="addCertForm.student_email"
            :options="courses"
            required>
          </b-form-select>
        </b-form-group>
        <b-form-group id="form-author-group"
                    label="Mentor:"
                    label-for="form-author-input">
          <b-form-select
            id="form-course-group"
            v-model="addCertForm.student_email"
            :options="mentors"
            required>
          </b-form-select>
        </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addCertForm.student_email" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      certs: [],
      addCertForm: {
        student_fname: '',
        student_lname: '',
        student_email: '',
        course: 's',
      },
      courses: ['dasds'],
      mentors: ['Tim', 'Janique'],
    };
  },
  methods: {
    getCerts() {
      const path = 'http://localhost:50000/api/certificate/all';
      axios.get(path)
        .then((res) => {
          this.certs = res.data.certs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    getCourses() {
      const path = 'http://localhost:50000/api/crud/course';
      axios.get(path)
        .then((res) => {
          this.courses = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  addCert(payload) {
    const path = 'http://localhost:50000/books';
    axios.post(path, payload)
      .then(() => {
        this.getCerts();
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
        this.getCerts();
      });
  },
  initForm() {
    this.addCertForm.student_fname = '';
    this.addCertForm.student_lname = '';
    this.addCertForm.student_email = [];
  },
  onSubmit(evt) {
    evt.preventDefault();
    this.$refs.addCertModal.hide();
    let read = false;
    if (this.addCertForm.read[0]) read = true;
    const payload = {
      fname: this.addCertForm.student_fname,
      lname: this.addCertForm.student_lname,
      read, // property shorthand
    };
    this.addCert(payload);
    this.initForm();
  },
  onReset(evt) {
    evt.preventDefault();
    this.$refs.addCertModal.hide();
    this.initForm();
  },

  created() {
    this.getCerts();
    this.getCourses();
  },
};
</script>
