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
      fbLabel: '',
      feedback: '',
      error: null,
      labels: [],
      predictions: []
    };

    this.state.labels = this.getLabels();
    this.handleInfer = this.handleInfer.bind(this);
    this.textHandle = this.textHandle.bind(this);
    this.radioHandle = this.radioHandle.bind(this);
    this.handleFeedback = this.handleFeedback.bind(this);
  }

  getLabels() {
      const labelsUrl = 'http://0.0.0.0:8000/labels';
      return ['fantasy', 'mystery', 'general'];
  }

  handleInfer() {
    const inferUrl = 'http://0.0.0.0:8000/predict';
    const payload = {text: this.state.text};
    fetch(inferUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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

  handleFeedback() {
    const feedbackUrl = 'http://0.0.0.0:80/feedback';
    const payload = {'label': this.state.fbLabel, 'text': this.state.text};
    fetch(feedbackUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload) // body data type must match "Content-Type" header
    })
    .then(res => res.json())
    .then(
        (result) => {
          // console.log(result);
        },
        (error) => {
          this.setState({
            error: error
          });
        }
      )
  }

  textHandle(e) {
    this.setState({text: e.target.value});
  }

  radioHandle(e) {
    this.setState({fbLabel: e.target.value});
  }

  render() {
    return (
      <Container className="p-3">
        <Form>
          <Form.Label>Example textarea</Form.Label>
          <Form.Control as="textarea" rows={3} value={this.state.text} onChange={this.textHandle}/>
          <Button variant="dark" onClick={this.handleInfer}>Infer!</Button>{' '}
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

        <Form>
          <Form.Label>Feedback</Form.Label>
          {this.state.labels.map((label) =>
              <Form.Check type="radio" id={label.id} label={label} value={label} onChange={this.radioHandle}/>
          )}
          <Button variant="dark" onClick={this.handleFeedback}>Submit Feedback</Button>{' '}
        </Form>


      </Container>
    )
  };
}

export default App;
