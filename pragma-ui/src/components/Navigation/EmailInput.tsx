import classNames from "classnames";
import React, { ChangeEvent, useState } from "react";
import styles from "./styles.module.scss";
import { ArrowRightIcon } from "@heroicons/react/outline";
import LightGreenUpper from "../common/LightGreenUpperText";
import PopupComponent from "../common/Popup";

interface InputProps {
  placeholderText: string;
  className?: string;
}

const InputComponent: React.FC<InputProps> = ({
  placeholderText,
  className,
}) => {
  const [email, setEmail] = useState<string>("");
  const [isValidEmail, setIsValidEmail] = useState<boolean>(true);
  const [isCheckboxChecked, setIsCheckboxChecked] = useState<boolean>(false);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleCheckboxChange = (e: ChangeEvent<HTMLInputElement>) => {
    setIsCheckboxChecked(e.target.checked);
  };

  const validateEmail = () => {
    const emailPattern = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    const isValid = emailPattern.test(email);
    setIsValidEmail(isValid);
    if (isValid) {
      setIsSubmitted(true); // Set to true if email is valid
    }
  };

  const handleButtonClick = () => {
    if (!isCheckboxChecked) {
      alert("Please tick the box");
      return;
    }
    validateEmail();
  };

  return (
    <div>
      <div className="flex flex-row justify-between gap-3">
        <input
          type="text"
          value={email}
          onChange={handleInputChange}
          placeholder={placeholderText}
          className={classNames(className, styles.input)}
        />
        <button
          className="ml-auto cursor-pointer rounded-full border border-LightGreenFooter bg-transparent p-2 text-LightGreenFooter hover:bg-LightGreenFooter hover:text-darkGreen"
          onClick={handleButtonClick}
        >
          <ArrowRightIcon className="w-3 cursor-pointer" />
        </button>
      </div>
      {!isValidEmail && <p style={{ color: "red" }}>Invalid email format</p>}
      {isSubmitted && (
        <PopupComponent
          title="Email submitted successfully"
          text="You will now start recieving emails from Pragma."
        />
      )}
      <label className={classNames("flex gap-3 pt-4", styles.checkbox)}>
        <input
          type="checkbox"
          checked={isCheckboxChecked}
          onChange={handleCheckboxChange}
          className={styles.checkbox}
        />
        <span className={styles.checkmark}></span>
        <LightGreenUpper>I agree with the privacy policy.</LightGreenUpper>
      </label>
    </div>
  );
};

export default InputComponent;
