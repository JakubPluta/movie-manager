import React from "react";

interface Props {
  title: string;
  children: React.ReactNode;
}

const ActorSelectorList = ({ title, children }: Props) => {
  return (
    <div className="m-2 w-1/2">
      <div>
        <h2 className="text-center text-lg font-bold">{title}</h2>
      </div>
      <div>{children}</div>
    </div>
  );
};

export default ActorSelectorList;
