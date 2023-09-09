import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

const HomePage = () => {
  return (
    <div>
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" fontWeight="bold" component="h2" gutterBottom>
          Welcome to Time Capsule Investor!
        </Typography>

        <section>
          <Typography variant="body1" fontFamily="Roboto" fontSize="20px" gutterBottom>
            The Time Capsule investor lets you see how much a hypothetical historical investment would be worth today.
            Find out how much money you would have made by investing in <span style={{fontWeight:"bold"}}>Nifty50</span> or
            <span style={{fontWeight:"bold"}}> s&p500 </span> stocks until 25 years ago.
          </Typography>
        </section>

        <section>
          <Typography variant="h5" fontWeight="bold" component="h3" gutterBottom>
            How It Works ??
          </Typography>
          <Typography variant="body1" gutterBottom>
            Here's how Time Capsule investor works:
          </Typography>
          <ul>
            <li>
              <Typography variant="body1">
                Create a bucket with stocks of your choice.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                Set a purchase time period (in years).
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                Set the investment amount for the bucket. This amount is spread across the bucket stocks uniformly.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                The Time Investment Calculator computes how many shares you could have purchased at the given date using historical stock data.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                The result shows you the value of your shares at today’s market price. This is the amount of money you would have made if you purchased this stock on the date you selected.
              </Typography>
            </li>
          </ul>
        </section>

        <section>
          <Typography variant="body1" fontWeight="bold">
          **Time Capsule Investor assumes that you can buy stocks in fractional units. 
          <br />
          **Return calculations do not include reinvested cash dividends.
          </Typography>
        </section>
      </Container>
    </div>
  );
};

export default HomePage;