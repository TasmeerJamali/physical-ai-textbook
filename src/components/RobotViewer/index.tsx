import React, { useState, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Environment, ContactShadows } from '@react-three/drei';
import styles from './styles.module.css';

// --- 3D Robot Components ---

function Base() {
    return (
        <group>
            {/* Main Base Cylinder */}
            <mesh position={[0, 0.25, 0]}>
                <cylinderGeometry args={[1, 1.2, 0.5, 32]} />
                <meshStandardMaterial color="#2d3436" metalness={0.8} roughness={0.2} />
            </mesh>
            {/* Platform */}
            <mesh position={[0, -0.1, 0]}>
                <boxGeometry args={[4, 0.2, 4]} />
                <meshStandardMaterial color="#636e72" />
            </mesh>
        </group>
    );
}

function Link({ position, rotation, length, color, children }: any) {
    return (
        <group position={position} rotation={rotation}>
            {/* The Link Geometry */}
            <mesh position={[0, length / 2, 0]}>
                <boxGeometry args={[0.4, length, 0.4]} />
                <meshStandardMaterial color={color} metalness={0.6} roughness={0.4} />
            </mesh>
            {/* Joint Visual at the end */}
            <mesh position={[0, length, 0]} rotation={[Math.PI / 2, 0, 0]}>
                <cylinderGeometry args={[0.3, 0.3, 0.5, 16]} />
                <meshStandardMaterial color="#b2bec3" />
            </mesh>
            {/* Child Link attached at the end */}
            <group position={[0, length, 0]}>
                {children}
            </group>
        </group>
    );
}

function EndEffector() {
    return (
        <group>
            <mesh position={[0, 0.2, 0]}>
                <boxGeometry args={[0.2, 0.4, 0.2]} />
                <meshStandardMaterial color="#d63031" />
            </mesh>
            {/* Grippers */}
            <mesh position={[-0.1, 0.5, 0]}>
                <boxGeometry args={[0.05, 0.4, 0.1]} />
                <meshStandardMaterial color="#2d3436" />
            </mesh>
            <mesh position={[0.1, 0.5, 0]}>
                <boxGeometry args={[0.05, 0.4, 0.1]} />
                <meshStandardMaterial color="#2d3436" />
            </mesh>
        </group>
    );
}

function RobotArm({ jointAngles }: { jointAngles: number[] }) {
    // jointAngles: [base, shoulder, elbow, wrist]

    return (
        <group position={[0, 0, 0]}>
            <Base />

            {/* Joint 1: Base Rotation (Y-axis) */}
            <group rotation={[0, jointAngles[0], 0]} position={[0, 0.5, 0]}>

                {/* Joint 2: Shoulder (Z-axis) */}
                <Link position={[0, 0, 0]} rotation={[0, 0, jointAngles[1]]} length={2} color="#0984e3">

                    {/* Joint 3: Elbow (Z-axis) */}
                    <Link position={[0, 0, 0]} rotation={[0, 0, jointAngles[2]]} length={1.5} color="#00b894">

                        {/* Joint 4: Wrist (Y-axis) */}
                        <group rotation={[0, jointAngles[3], 0]}>
                            <EndEffector />
                        </group>

                    </Link>
                </Link>
            </group>
        </group>
    );
}

// --- Main Component ---

export default function RobotViewer(): JSX.Element {
    const [joints, setJoints] = useState([0, 0.5, -1, 0]); // Initial pose

    const updateJoint = (index: number, value: number) => {
        const newJoints = [...joints];
        newJoints[index] = parseFloat(value.toString());
        setJoints(newJoints);
    };

    return (
        <div className={styles.container}>
            <div className={styles.canvasContainer}>
                <Canvas camera={{ position: [4, 4, 4], fov: 50 }} shadows>
                    <Environment preset="city" />
                    <ambientLight intensity={0.5} />
                    <pointLight position={[10, 10, 10]} intensity={1} castShadow />

                    <RobotArm jointAngles={joints} />

                    <Grid infiniteGrid fadeDistance={30} sectionColor="#4a4a4a" cellColor="#6a6a6a" />
                    <ContactShadows opacity={0.5} scale={10} blur={2} far={4} />
                    <OrbitControls makeDefault minPolarAngle={0} maxPolarAngle={Math.PI / 2} />
                </Canvas>
            </div>

            <div className={styles.controls}>
                <h3>🎮 Robot Controls (Forward Kinematics)</h3>

                <div className={styles.controlGroup}>
                    <label>Base Rotation (J1)</label>
                    <input
                        type="range" min="-3.14" max="3.14" step="0.01"
                        value={joints[0]} onChange={(e) => updateJoint(0, parseFloat(e.target.value))}
                    />
                    <span>{joints[0].toFixed(2)} rad</span>
                </div>

                <div className={styles.controlGroup}>
                    <label>Shoulder (J2)</label>
                    <input
                        type="range" min="-1.57" max="1.57" step="0.01"
                        value={joints[1]} onChange={(e) => updateJoint(1, parseFloat(e.target.value))}
                    />
                    <span>{joints[1].toFixed(2)} rad</span>
                </div>

                <div className={styles.controlGroup}>
                    <label>Elbow (J3)</label>
                    <input
                        type="range" min="-2.5" max="2.5" step="0.01"
                        value={joints[2]} onChange={(e) => updateJoint(2, parseFloat(e.target.value))}
                    />
                    <span>{joints[2].toFixed(2)} rad</span>
                </div>

                <div className={styles.controlGroup}>
                    <label>Wrist Rotate (J4)</label>
                    <input
                        type="range" min="-3.14" max="3.14" step="0.01"
                        value={joints[3]} onChange={(e) => updateJoint(3, parseFloat(e.target.value))}
                    />
                    <span>{joints[3].toFixed(2)} rad</span>
                </div>

                <div className={styles.info}>
                    <p><strong>Tip:</strong> Drag to rotate view. Scroll to zoom.</p>
                </div>
            </div>
        </div>
    );
}
