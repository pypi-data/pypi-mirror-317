from __future__ import annotations

__author__ = 'Tobia Petrolini'
__file__ = 'elements.py'

from .equations import *


class Point():
    # Represents a point in 2D space, with x and y coordinates.
    def __init__(self, x: int | float | str | sp.Expr | None, y: int | float | str | sp.Expr | None):
        """
        Initializes the Point object with x and y coordinates.

        Args:
            x (int | float | str | sp.Expr | None): The x-coordinate of the point.
            y (int | float | str | sp.Expr | None): The y-coordinate of the point.
        """
        self.x = x
        self.y = y

        # Convert x and y to symbolic values
        self.x = sympy_value(self.x, 'x')
        self.y = sympy_value(self.y, 'y')

        # Store coordinates as a tuple
        self.cordinates = self.x, self.y

        # Determine the quadrant of the point
        if float(self.x) > 0 and float(self.y) > 0:
            self.quadrant = 1
        elif float(self.x) < 0 and float(self.y) > 0:
            self.quadrant = 2
        elif float(self.x) < 0 and float(self.y) < 0:
            self.quadrant = 3
        elif float(self.x) > 0 and float(self.y) < 0:
            self.quadrant = 4

    def __str__(self) -> str:
        """
        Returns a string representation of the coordinates.

        Returns:
            str: A string representing the point as (x, y).
        """
        return f"{self.cordinates}"

    def isorigin(self) -> bool:
        """
        Checks if the point is the origin.

        Returns:
            bool: True if the point is the origin, False otherwise.
        """
        return float(self.x) == 0 and float(self.y) == 0

    def distancePoint(self, point: 'Point') -> sp.Expr:
        """
        Calculate the Euclidean distance to another point.

        Args:
            point (Point): The other point to calculate the distance from.

        Returns:
            sp.Expr: The distance as a SymPy expression.
        """
        return sp.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

    def distanceLine(self, line: 'Line') -> sp.Expr:
        """
        Calculate the perpendicular distance from the point to a line.

        Args:
            line (Line): The line to calculate the distance from.

        Returns:
            sp.Expr: The distance as a SymPy expression.
        """
        return sp.Abs(line.a*self.x + line.b*self.y + line.c) / sp.sqrt(line.a**2 + line.b**2)

    def ison(self, element: 'Point' | 'Line' | 'Segment') -> bool:
        """
        Determine if the point lies on a given geometric element.

        Args:
            element (Point | Line | Segment): The geometric element.

        Returns:
            bool: True if the point lies on the element.
        """
        if isinstance(element, Point):
            return element.cordinates == self.cordinates
        elif isinstance(element, Line):
            # Check if the point satisfies the line equation
            return sp.simplify(element.a * self.x + element.b * self.y + element.c) == 0
        elif isinstance(element, Segment):
            # Check if the point lies within the segment's endpoints and on its line
            min_x = min(element.point1.x, element.point2.x)
            max_x = max(element.point1.x, element.point2.x)
            min_y = min(element.point1.y, element.point2.y)
            max_y = max(element.point1.y, element.point2.y)
            return self.ison(element.line) and (self.x >= min_x and self.x <= max_x) and (self.y >= min_y and self.y <= max_y)

    @staticmethod
    def findPoint(line: 'Line', point: 'Point', distance: int | float | str | sp.Expr) -> tuple['Point', 'Point | None']:
        """
        Find two points on a line at a specific distance from a reference point.

        Args:
            line (Line): The line on which to find the points.
            point (Point): The reference point.
            distance (int | float | str | sp.Expr): The desired distance from the reference point.

        Returns:
            tuple[Point, Point]: A tuple containing two points at the given distance.

        Raises:
            ValueError: If there are no possible points at the given distance.
        """
        distance = sympy_value(distance, 'distance')

        # Equation of a circle around the reference point
        circle_eq = sp.Eq((sp.Symbol('x') - point.x)**2 +
                          (sp.Symbol('y') - point.y)**2, distance**2)

        # Solve for intersection points between the circle and line
        sol = list(sp.solve([circle_eq, line.equation],
                            (sp.Symbol('x'), sp.Symbol('y'))))

        if not isinstance(sol[0][0], sp.Expr):
            raise ValueError(
                'There is no point at that distance that lies on the line')
        elif len(sol) == 1:
            return Point(sol[0][0], sol[0][1]), None
        else:
            return Point(sol[0][0], sol[0][1]), Point(sol[1][0], sol[1][1])


ORIGIN = Point(sp.Integer(0), sp.Integer(0))


class Line():
    # Represents a line in 2D space, defined by an equation.
    def __init__(self, equation: str | sp.Equality):
        """
        Initializes the Line object from an equation.

        Args:
            equation (str | sp.Equality): The equation defining the line.

        Raises:
            ValueError: If the provided equation format is invalid.
        """
        self.equation = equation

        # Process the equation input
        if isinstance(self.equation, str):
            self.equation = read_equation(self.equation)
        elif isinstance(self.equation, sp.Equality):
            pass
        else:
            raise ValueError("equation must be an Equality or str")

        # Determine the implicit form and coefficients
        if 'y' in str(self.equation):
            self.equation = sp.Eq(expression('y'), expression(
                str(sp.solve(self.equation, 'y')[0])))

            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1]
                                for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            # Simplify the implicit equation
            self.implicitEquation = sp.Eq(scaled_lhs.simplify(), 0)

            # Calculate slope and intercept
            self.slope = sp.simplify(
                sp.diff(self.equation.rhs, sp.Symbol('x')))
            self.intercept = sp.solve(self.equation, 'y')[0].subs('x', 0)

            # Extract coefficients for implicit form
            x, y = sp.symbols('x y')
            self.a = self.implicitEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = self.implicitEquation.lhs.as_coefficients_dict().get(y, 0)
            self.c = self.implicitEquation.lhs.as_coefficients_dict().get(1, 0)
        else:
            # Vertical line processing
            self.equation = sp.Eq(expression('x'), expression(
                str(sp.solve(self.equation, 'x')[0])))

            lhs, rhs = self.equation.lhs, self.equation.rhs
            lcm_denoms = sp.lcm([term.as_numer_denom()[1]
                                for term in (lhs - rhs).as_ordered_terms()])
            scaled_lhs = (lhs - rhs) * lcm_denoms

            self.implicitEquation = sp.Eq(scaled_lhs.simplify(), 0)
            x = sp.symbols('x')
            self.a = self.implicitEquation.lhs.as_coefficients_dict().get(x, 0)
            self.b = sp.Integer(0)
            self.c = self.implicitEquation.lhs.as_coefficients_dict().get(1, 0)
            self.slope = sp.oo
            self.intercept = None

    def __str__(self) -> str:
        """
        Returns the equation of the line as a string.

        Returns:
            str: The line equation in string format.
        """
        return f'{self.equation.lhs} = {self.equation.rhs}'

    def isHorizontal(self) -> bool:
        """
        Check if the line is horizontal.

        Returns:
            bool: True if the line is horizontal.
        """
        return self.slope == 0

    def isVertical(self) -> bool:
        """
        Check if the line is vertical.

        Returns:
            bool: True if the line is vertical.
        """
        return self.slope == sp.oo

    def isParallel(self, line: 'Line') -> bool:
        """
        Check if the line is parallel to another line.

        Args:
            line (Line): The other line.

        Returns:
            bool: True if the lines are parallel.
        """
        return self.slope == line.slope

    def isPerpendicular(self, line: 'Line') -> bool:
        """
        Check if the line is perpendicular to another line.

        Args:
            line (Line): The other line.

        Returns:
            bool: True if the lines are perpendicular.
        """
        return self.slope * line.slope == -1

    def intersection(self, line: 'Line') -> Point:
        """
        Calculate the intersection point with another line.

        Args:
            line (Line): The other line.

        Returns:
            Point: The intersection point.
        """
        x, y = sp.symbols('x y')
        sol = sp.solve([self.equation, line.equation], (x, y))
        return Point(sol[x], sol[y])

    def isPerpendicularBisector(self, segment: 'Segment') -> bool:
        """
        Check if the line is the axis of a given segment.

        Args:
            segment (Segment): The segment to check.

        Returns:
            bool: True if the line is the axis of the segment.
        """
        return str(self.equation) == str(segment.perpendicularBisector.equation)

    def isBisector(self, line1: 'Line', line2: 'Line') -> bool:
        """
        Check if the line is the bisector of the angle between two other lines.

        Args:
            line1 (Line): The first line.
            line2 (Line): The second line.

        Returns:
            bool: True if the line is the bisector of the two lines.
        """
        intersection_point = line1.intersection(line2)

        # Determine a test point slightly offset from the intersection
        if not self.isVertical():
            test_point = Point(intersection_point.x + 1,
                               intersection_point.y + self.slope)
        else:
            test_point = Point(intersection_point.x, intersection_point.y + 1)

        # Calculate distances from the test point to the two lines
        distance_to_line1 = test_point.distanceLine(line1)
        distance_to_line2 = test_point.distanceLine(line2)

        # Check if distances are equal
        return sp.simplify(distance_to_line1 - distance_to_line2) == 0

    def findParallel(self, point: Point) -> 'Line':
        """
        Find a parallel line that passes through a given point.

        Args:
            point (Point): The point through which the parallel line passes.

        Returns:
            Line: The parallel line.
        """
        if self.isVertical():
            return Line(sp.Eq(expression('x'), point.x))
        else:
            intercept = point.y - self.slope * point.x
            return Line(sp.Eq(expression('y'), self.slope * expression('x') + intercept))

    def findPerpendicular(self, point: Point) -> 'Line':
        """
        Find a perpendicular line that passes through a given point.

        Args:
            point (Point): The point through which the perpendicular line passes.

        Returns:
            Line: The perpendicular line.
        """
        if self.isVertical():
            return Line(sp.Eq(expression('y'), point.y))
        elif self.isHorizontal():
            return Line(sp.Eq(expression('x'), point.x))
        else:
            perpendicular_slope = -1 / self.slope
            intercept = point.y - perpendicular_slope * point.x
            return Line(sp.Eq(expression('y'), perpendicular_slope * expression('x') + intercept))

    def findBisector(self, line: 'Line') -> tuple['Line', 'Line']:
        """
        Find the bisectors of the angles formed between the current line and another line.

        Args:
            line (Line): The other line.

        Returns:
            tuple[Line, Line]: The two angle bisectors as lines.
        """
        x, y = sp.symbols('x y')

        # Calculate distance expressions for each line
        distance_self = (self.a * x + self.b * y + self.c) / \
            sp.sqrt(self.a**2 + self.b**2)
        distance_line = (line.a * x + line.b * y + line.c) / \
            sp.sqrt(line.a**2 + line.b**2)

        # Form equations for the angle bisectors
        eq1 = sp.Eq(distance_self, distance_line)
        eq2 = sp.Eq(distance_self, -distance_line)

        # Solve for the bisectors
        if not self.isVertical():
            solutions1 = sp.solve(eq1, y)
            solutions2 = sp.solve(eq2, y)
            solutions = solutions1 + solutions2
        else:
            solutions1 = sp.solve(eq1, x)
            solutions2 = sp.solve(eq2, x)
            solutions = solutions1 + solutions2

        if len(solutions) == 2:
            line1 = Line(sp.Eq(y, solutions[0])) if not self.isVertical(
            ) else Line(sp.Eq(x, solutions[0]))
            line2 = Line(sp.Eq(y, solutions[1])) if not self.isVertical(
            ) else Line(sp.Eq(x, solutions[1]))
            return line1, line2
        else:
            return Line(sp.Eq(y, solutions[0])) if not self.isVertical() else Line(sp.Eq(x, solutions[0]))

    @staticmethod
    def findLine(point1: Point | None = None, point2: Point | None = None, slope: int | float | str | sp.Expr | None = None, intercept: int | float | str | sp.Expr | None = None) -> 'Line':
        """
        Generate a line based on given parameters.

        Args:
            point1 (Point | None): The first point on the line.
            point2 (Point | None): The second point on the line.
            slope (int | float | str | sp.Expr | None): The slope of the line.
            intercept (int | float | str | sp.Expr | None): The y-intercept of the line.

        Returns:
            Line: The constructed line object.

        Raises:
            ValueError: If sufficient parameters are not provided.
        """
        is_vertical = False

        # Check if the line is vertical based on the slope or point alignment
        if slope == sp.oo or (point1 and point2 and point1.x == point2.x):
            is_vertical = True

        if intercept is not None:
            intercept = sympy_value(intercept, 'intercept')

        if is_vertical:
            if point1:
                return Line(sp.Eq(expression('x'), point1.x))
            elif point2:
                return Line(sp.Eq(expression('x'), point2.x))
            elif intercept is not None:
                return Line(sp.Eq(expression('x'), intercept))
            else:
                raise ValueError(
                    "One of point1, point2, or intercept must be provided.")
        else:
            # Calculate slope or intercept when necessary
            if point1 and point2:
                slope = (point2.y - point1.y) / (point2.x - point1.x)
                intercept = point1.y - slope * point1.x
            elif point1 and slope is not None:
                intercept = point1.y - slope * point1.x
            elif point2 and slope is not None:
                intercept = point2.y - slope * point2.x
            elif slope is not None and intercept is not None:
                pass
            else:
                raise ValueError("At least two parameters must be provided.")

        return Line(sp.Eq(expression('y'), slope * expression('x') + intercept))


X_AXIS = Line(equation('y = 0'))
Y_AXIS = Line(equation('x = 0'))
BISECTOR_1_3 = Line(equation('y = x'))
BISECTOR_2_4 = Line(equation('y = -x'))


class Segment:
    # Represents a line segment between two points.
    def __init__(self, point1: Point, point2: Point):
        """
        Initializes the Segment object with two endpoints.

        Args:
            point1 (Point): The first endpoint of the segment.
            point2 (Point): The second endpoint of the segment.
        """
        self.point1 = point1
        self.point2 = point2

        # Calculate segment properties
        self.length = self.point1.distancePoint(self.point2)
        self.middle = Point((self.point1.x + self.point2.x) / 2,
                            (self.point1.y + self.point2.y) / 2)
        self.line = Line.findLine(self.point1, self.point2)
        self.perpendicularBisector = self.line.findPerpendicular(self.middle)
