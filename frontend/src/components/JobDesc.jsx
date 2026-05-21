import { Fragment } from "react";

export default function JobDesc({ text }) {
    const types = Object.freeze({
        TEXT: "text",
        HEADER: "header",
        BULLET_GROUP: "bulletGroup",
        SPACE: "space",
    });

    function formatJobDesc(jobDesc) {
        const groups = [];
        let prevHeaderText = null;
        let prevWasBullet = false;
        let bulletGroup = null;
        const commonBulletHeaders = new Set([
            "minimum qualifications",
            "basic qualifications",
            "preferred qualifications",
            "minimum requirements",
            "Minimum requirements",
            "preferred requirements",
            "responsibilities",
        ]);

        for (const line of jobDesc.split("\n")) {
            const headerScore = scoreLine(line);
            const curIsHeader = headerScore >= 3;
            const curIsBullet =
                (prevHeaderText &&
                    (commonBulletHeaders.has(prevHeaderText.toLowerCase()) ||
                        commonBulletHeaders.has(
                            prevHeaderText.slice(0, -1),
                        ))) ||
                (prevWasBullet && !curIsHeader && line.length != 0);

            bulletGroup = pushLine(
                groups,
                bulletGroup,
                line,
                curIsBullet,
                curIsHeader,
                prevHeaderText,
            );

            prevHeaderText = curIsHeader ? line : null;
            prevWasBullet = curIsBullet;
        }
        console.log(groups);
        return groups;
    }

    function scoreLine(line) {
        let score = 0;
        if (line.at(-1) === ":") score += 3;
        if (line.length <= 40) score += 1;
        if (isTitleCase(line)) score += 2;
        if (isCommonHeader(line)) score += 2;
        return score;
    }

    function isTitleCase(line) {
        const wordExceptions = new Set(["the", "of"]);
        const tokens = line.split(" ");
        if (!tokens[0]) return false;
        for (const token of tokens) {
            if (wordExceptions.has(token)) continue;
            if (token) if (token === token.toLowerCase()) return false;
        }
        return true;
    }

    function isCommonHeader(line) {
        const commonHeaders = new Set([
            "about the role",
            "about the team",
            "minimum qualifications",
            "preferred qualifications",
            "minimum requirements",
            "preferred requirements",
            "who we are",
            "working remotely at stripe",
        ]);
        if (
            commonHeaders.has(line.toLowerCase()) ||
            commonHeaders.has(line.slice(0, -1).toLowerCase())
        )
            return true;
        return false;
    }

    //returns bulletGroup so it saves its state
    function pushLine(
        groups,
        bulletGroup,
        line,
        curIsBullet,
        curIsHeader,
        prevHeaderText,
    ) {
        if (curIsBullet) {
            if (!bulletGroup) {
                bulletGroup = { type: types.BULLET_GROUP, bullets: [] };
                groups.push(bulletGroup);
            }
            bulletGroup.bullets.push(line);
        } else {
            bulletGroup = null;
            let lineType = types.TEXT;
            if (curIsHeader) lineType = types.HEADER;
            else if (line.length === 0) lineType = types.SPACE;
            if (lineType === types.SPACE && prevHeaderText) return;
            groups.push({ type: lineType, text: line });
        }
        return bulletGroup;
    }

    const formattedJobDesc = formatJobDesc(text).map((group, i) => {
        switch (group.type) {
            case "bulletGroup":
                return (
                    <ul key={i} className="list-disc pl-6">
                        {group.bullets.map((bullet, j) => (
                            <li key={j}>{bullet}</li>
                        ))}
                    </ul>
                );
            case "header":
                if (i === 0) return <h2 key={i + 0.5}>{group.text}</h2>;
                return (
                    <Fragment key={i}>
                        <br />
                        <h2 key={i + 0.5}>{group.text}</h2>
                    </Fragment>
                );
            case "text":
                return <p key={i}>{group.text}</p>;
            default:
                return <br key={i} />;
        }
    });

    return <div id="jobDesc">{formattedJobDesc}</div>;
}
