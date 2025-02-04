  auto EigenToQMatrix4x4 = [](const Eigen::Matrix4f& eigenMatrix) -> QMatrix4x4 {
			return QMatrix4x4(
				eigenMatrix(0, 0), eigenMatrix(0, 1), eigenMatrix(0, 2), eigenMatrix(0, 3),
				eigenMatrix(1, 0), eigenMatrix(1, 1), eigenMatrix(1, 2), eigenMatrix(1, 3),
				eigenMatrix(2, 0), eigenMatrix(2, 1), eigenMatrix(2, 2), eigenMatrix(2, 3),
				eigenMatrix(3, 0), eigenMatrix(3, 1), eigenMatrix(3, 2), eigenMatrix(3, 3)
			);
		};

		auto QMatrix4x4ToEigen = [](const QMatrix4x4& qMatrix) -> Eigen::Matrix4f {
			return Eigen::Matrix4f{
				{qMatrix(0, 0), qMatrix(0, 1), qMatrix(0, 2), qMatrix(0, 3)},
				{qMatrix(1, 0), qMatrix(1, 1), qMatrix(1, 2), qMatrix(1, 3)},
				{qMatrix(2, 0), qMatrix(2, 1), qMatrix(2, 2), qMatrix(2, 3)},
				{qMatrix(3, 0), qMatrix(3, 1), qMatrix(3, 2), qMatrix(3, 3)}
			};
		};
