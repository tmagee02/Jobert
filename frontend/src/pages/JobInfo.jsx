import { useParams } from "react-router-dom";

export default function JobInfo() {
  const { jobId } = useParams();
  return <h1>Job Info {jobId}</h1>;
}
