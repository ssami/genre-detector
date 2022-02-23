import './App.css';
import React from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      text: '',
      error: null,
      isLoaded: false,
      predictions: []
    };

    this.handleForm = this.handleForm.bind(this);
    this.textHandle = this.textHandle.bind(this);
  }

  handleForm() {
    const payload = {text: this.state.text};
    console.log(payload);
    fetch('http://0.0.0.0:80/predict', {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      headers: {
        'Content-Type': 'application/json',
        // 'Accept': 'application/json'
      },
      body: JSON.stringify(payload) // body data type must match "Content-Type" header
    })
    .then(res => res.json())
    .then(
        (result) => {
          this.setState({
            isLoaded: true,
            predictions: JSON.parse(result)
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error: error
          });
        }
      )
  }

  textHandle(e) {
    this.setState({text: e.target.value});
  }

  render() {
    return (
      <Container className="p-3">
        <Form>
          <Form.Label>Example textarea</Form.Label>
          <Form.Control as="textarea" rows={3} value={this.state.text} onChange={this.textHandle}/>
          <Button variant="dark" onClick={this.handleForm}>Submit</Button>{' '}
        </Form>

        <Container className="p-3">
          {this.state.predictions.map((pred) =>
            <Card key={pred.id}>
              <Card.Body>
                <Card.Title>Predictions</Card.Title>
                <Card.Text>
                    Prediction: {pred[0]}
                  <br/>
                    Confidence score: {pred[1]}
                </Card.Text>
              </Card.Body>
            </Card>
          )}
        </Container>
      </Container>
    )
  };
}

export default App;
