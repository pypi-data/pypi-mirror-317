# 🐀 rodents



🐀 rodents is a command line tool that moves the mouse cursor randomly on the screen and performs random actions such as switching tabs or clicking on buttons. It is designed to simulate user activity and prevent screensavers or idle timeouts from activating.

## 📋 Requirements

- know how access the terminal on your computer, [here is a guide to use terminal on Mac](https://www.youtube.com/watch?v=FfT8OfMpARM)
- install pip on your computer, here is a [guide to install pip](https://www.youtube.com/watch?v=MuOy6I7ng_Q)

## 🚀 Installation

You can install 🐀 rodents using pip:

```
pip install rodents
```

## 🖱 Usage

To use 🐀 rodents, you can run the following command:

```
rodents --delay_mean <mean> --delay_std_dev <std_dev> --move_duration <duration>
```

This will make the movements of your mouse delayed in a way that follows a normal distribution so that there are no fixed intervals of movements to make it appear more human.


![Alt](images/normal_distribution.png)





💡 PROTIP: best if you open up a single browser with multiple tabs you want the program to cycle through.

The available options are:

- `--delay_mean`: Mean value for the delay pressing of keys in seconds. Default is 12.
- `--delay_std_dev`: Standard deviation for the delays. Default is 6.
- `--move_duration`: Duration of the mouse movement in seconds. Default is 0.5, this seems to look most natural.

For example, to run 🐀 rodents with a mean delay of 10, standard deviation of 5, and a movement duration of 1 second, you can use the following command:

```
rodents --delay_mean 10 --delay_std_dev 5 --move_duration 1
```

🛑 Stopping 🐀 rodents: press Ctrl + C in your terminal (Mac) or other similar hot-key to stop terminal execution.


## 🚨 Disclaimer

🐀 rodents is intended for educational and testing purposes only. It should not be used for any malicious activities. The developers of rodents are not responsible for any misuse or damage caused by this tool.

## License

🐀 rodents is released under the MIT License. 


## 🤝 Contributing

Thank you for considering contributing to 🐀 rodents! We welcome any contributions that can help improve the project and make it even more useful.

To contribute to 🐀 rodents, please follow these steps:

1. Find an issue you want to work on [here](https://github.com/espin086/rodents/issues) and comment on issue stating your desire to work on it, wait for moderator response Or create an issue for a new feature and wait for moderator response.
2. Fork the repository on GitHub.
3. Clone your forked repository to your local machine.
4. Create a new branch for your contribution.
5. Make your changes and improvements to the codebase.
6. Test your changes thoroughly.
7. Commit and push your changes to your forked repository.
8. Submit a pull request to the main repository.

Please ensure that your code follows best practices and is well-documented. We appreciate detailed commit messages and clear explanations of the changes you have made.

By contributing to 🐀 rodents, you agree to release your contributions under the MIT License.